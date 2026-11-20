# H2a 다시 재기 (11-20 아침 사용자: 캐시 재사용을 포인트로, 1번부터). 모델이 생성한 그대로(reasoning 포함) 다시 보내 후속 턴 재사용을 살린다.
#   K : H2a(--reasoning-echo all) + card-coding + --seed-per-rep, 6과제 x 5회. 접두사 x3h2k
#   짝: S1 체인의 x3s1c(H0 + card-coding, 같은 회차 · 같은 seed 42~46)를 대조로 쓴다(두 번 안 돌림). 다른 점은 reasoning 재전송 하나.
#   보는 것: 통과(짝 비교) · 엔진 로그의 재사용 토큰과 새로 읽은 토큰 · 실행 시간 · 강제 마지막 턴 · thinking 기록.
# 설정 고정 · 슬롯 확인 · nvidia-smi 는 s1-chain 과 같다. 끝 표시 '[h2k] done'.
param([int]$Context = 32768, [int]$Reps = 5, [int]$ExpectSlots = 63)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$engLog = "C:\strata-lab\engine\strata-qwen36-ctx$Context-h2k.log"
function Slots {
  if (-not (Test-Path $engLog)) { return -1 }
  $m = Select-String -Path $engLog -Pattern 'hybrid experts: (\d+) of 256' | Select-Object -Last 1
  if ($m) { return [int]$m.Matches[0].Groups[1].Value } else { return -1 }
}
function Start-Server {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context -Tag h2k" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-h2k.log" -RedirectStandardError "C:\strata-lab\engine\serve-h2k.err" -WindowStyle Hidden
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
    "[h2k] server start try $try (GPU used before $vram MiB) $(Get-Date -Format s)"
    $h = Start-Server
    $s = Slots
    "[h2k] server loaded=$($h.loaded) slots=$s (expect $ExpectSlots)"
    if ($s -eq $ExpectSlots) { break }
    "[h2k] 경고: 슬롯 수가 다름 - 다시 띄움"
  }
  return $h
}
"[h2k] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
"[h2k] power $((powercfg /getactivescheme) -join ' ')"
$gpu = Start-Process nvidia-smi -ArgumentList '--query-gpu=timestamp,temperature.gpu,clocks.sm,clocks.mem,power.draw,memory.used,clocks_event_reasons.active --format=csv -l 60 -f C:\strata-lab\engine\gpu-h2k.csv' -WindowStyle Hidden -PassThru
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$h = Ensure-Server
"[h2k] ready ctx $($h.max_context) $(Get-Date -Format s)"
$tasks = @('dg_group_names', 'marker_extras', 'version_bump', 'tags_platform_filter', 'metadata_extra_dupes', 'specifier_bounds')
$hb = @('--harness', 'H2a', '--tool-out', 'chars', '--reasoning-echo', 'all', '--final-turn', 'none', '--seed-per-rep')
$arms = @(
  @{n = 'K'; x = 'x3h2k'; a = $hb + @('--sampling', 'card-coding')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[h2k] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks @tasks --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[h2k] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
if ($gpu -and -not $gpu.HasExited) { Stop-Process -Id $gpu.Id -Force }
"[h2k] done $(Get-Date -Format s)"
