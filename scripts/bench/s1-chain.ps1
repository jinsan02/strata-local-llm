# S1 샘플링 A/B (11-19 합의): 하네스 H0 고정, 샘플링 세트만 다르게 번갈아 5회, X3 6과제.
#   G : --sampling card-general (지금: 1.0 / 0.95 / 20 / presence 1.5 / seed 42)   접두사 x3s1g
#   C : --sampling card-coding  (모델 카드 정밀 코딩: 0.6 / 0.95 / 20 / presence 0 / seed 42)   접두사 x3s1c
#   seed: --seed-per-rep (11-19 저녁 합의) 회차 r 은 두 조건 모두 seed 42+r-1 → 같은 회차끼리 짝 비교.
# 판정(11-19 합의): 과제 · 회차 짝 비교(부호 검정 · McNemar), 나빠졌다는 증거가 있으면 기각, 같으면 잡음 · 효율로.
# 설정 고정: 서버는 고정 키가 들어간 serve-ctx, 매 기동 뒤 엔진 로그의 expert 슬롯 수를 확인(32K = 63, 다르면 한 번 다시 띄움).
# GPU 상태는 engine\gpu-s1.csv 에 1분마다(온도 · 클럭 · 전력 · VRAM). 끝 표시 '[s1] done'.
param([int]$Context = 32768, [int]$Reps = 5, [int]$ExpectSlots = 63)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$engLog = "C:\strata-lab\engine\strata-qwen36-ctx$Context-s1.log"
function Slots {
  if (-not (Test-Path $engLog)) { return -1 }
  $m = Select-String -Path $engLog -Pattern 'hybrid experts: (\d+) of 256' | Select-Object -Last 1
  if ($m) { return [int]$m.Matches[0].Groups[1].Value } else { return -1 }
}
function Start-Server {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context -Tag s1" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-s1.log" -RedirectStandardError "C:\strata-lab\engine\serve-s1.err" -WindowStyle Hidden
  $h = $null
  for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 5
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
  }
  return $h
}
function Ensure-Server {
  $h = $null
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if ($h -and $h.loaded -and $h.max_context -eq $Context) { return $h }
  for ($try = 1; $try -le 2; $try++) {
    $vram = (& nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits) -join ''
    "[s1] server start try $try (GPU used before $vram MiB) $(Get-Date -Format s)"
    $h = Start-Server
    $s = Slots
    "[s1] server loaded=$($h.loaded) slots=$s (expect $ExpectSlots)"
    if ($s -eq $ExpectSlots) { break }
    "[s1] 경고: 슬롯 수가 다름 - 다시 띄움"
  }
  return $h
}
"[s1] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
$power = (powercfg /getactivescheme) -join ' '
"[s1] power $power"
$gpu = Start-Process nvidia-smi -ArgumentList '--query-gpu=timestamp,temperature.gpu,clocks.sm,clocks.mem,power.draw,memory.used,clocks_event_reasons.active --format=csv -l 60 -f C:\strata-lab\engine\gpu-s1.csv' -WindowStyle Hidden -PassThru
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$h = Ensure-Server
"[s1] ready ctx $($h.max_context) $(Get-Date -Format s)"
$tasks = @('dg_group_names', 'marker_extras', 'version_bump', 'tags_platform_filter', 'metadata_extra_dupes', 'specifier_bounds')
$hb = @('--harness', 'H0', '--tool-out', 'chars', '--reasoning-echo', 'none', '--final-turn', 'none', '--seed-per-rep')
$arms = @(
  @{n = 'G'; x = 'x3s1g'; a = $hb + @('--sampling', 'card-general')},
  @{n = 'C'; x = 'x3s1c'; a = $hb + @('--sampling', 'card-coding')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[s1] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks @tasks --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[s1] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
if ($gpu -and -not $gpu.HasExited) { Stop-Process -Id $gpu.Id -Force }
"[s1] done $(Get-Date -Format s)"
