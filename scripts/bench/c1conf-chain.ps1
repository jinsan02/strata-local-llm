# C1(반복 읽기 막기) 확인 (11-19 밤): hadd 에서 H0 5/12 vs H0+C1 9/12 (짝 4:0, seed 고정이라 독립성 약함) → seed 회차로 다시 본다.
#   B : H0            접두사 x3c1b
#   R : H0 + C1       접두사 x3c1r (--reread-guard on)
# 두 조건 모두 --seed-per-rep: 회차 r 은 seed 42+r-1 → 같은 회차끼리 짝 비교(McNemar · 부호 검정). 샘플링은 card-general(기본).
# thinking 관측 기록(patch_think) 이 들어간 run_x3 로 돈다. 설정 고정 · 슬롯 확인 · nvidia-smi 는 s1-chain 과 같다. 끝 표시 '[c1] done'.
param([int]$Context = 32768, [int]$Reps = 4, [int]$ExpectSlots = 63)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$engLog = "C:\strata-lab\engine\strata-qwen36-ctx$Context-c1.log"
function Slots {
  if (-not (Test-Path $engLog)) { return -1 }
  $m = Select-String -Path $engLog -Pattern 'hybrid experts: (\d+) of 256' | Select-Object -Last 1
  if ($m) { return [int]$m.Matches[0].Groups[1].Value } else { return -1 }
}
function Start-Server {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context -Tag c1" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-c1.log" -RedirectStandardError "C:\strata-lab\engine\serve-c1.err" -WindowStyle Hidden
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
    "[c1] server start try $try (GPU used before $vram MiB) $(Get-Date -Format s)"
    $h = Start-Server
    $s = Slots
    "[c1] server loaded=$($h.loaded) slots=$s (expect $ExpectSlots)"
    if ($s -eq $ExpectSlots) { break }
    "[c1] 경고: 슬롯 수가 다름 - 다시 띄움"
  }
  return $h
}
"[c1] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
"[c1] power $((powercfg /getactivescheme) -join ' ')"
$gpu = Start-Process nvidia-smi -ArgumentList '--query-gpu=timestamp,temperature.gpu,clocks.sm,clocks.mem,power.draw,memory.used,clocks_event_reasons.active --format=csv -l 60 -f C:\strata-lab\engine\gpu-c1.csv' -WindowStyle Hidden -PassThru
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$h = Ensure-Server
"[c1] ready ctx $($h.max_context) $(Get-Date -Format s)"
$tasks = @('dg_group_names', 'marker_extras', 'version_bump', 'tags_platform_filter', 'metadata_extra_dupes', 'specifier_bounds')
$hb = @('--harness', 'H0', '--tool-out', 'chars', '--reasoning-echo', 'none', '--final-turn', 'none', '--seed-per-rep')
$arms = @(
  @{n = 'B'; x = 'x3c1b'; a = $hb},
  @{n = 'R'; x = 'x3c1r'; a = $hb + @('--reread-guard', 'on')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[c1] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks @tasks --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[c1] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
if ($gpu -and -not $gpu.HasExited) { Stop-Process -Id $gpu.Id -Force }
"[c1] done $(Get-Date -Format s)"
