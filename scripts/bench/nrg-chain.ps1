# 11-21 밤 체인 (사용자: 선택 끝나면 밤 모드, 자는 동안 다음 것): M0 · E0 · 32K · H0 + card-coding 기준 위에서 두 가지.
#   RT : --run-tests on (Q15, 다음 할 일 25-2), 6과제 x 5회, 접두사 x3rt. 대조 = S1 의 x3s1c(같은 회차 · 같은 seed 42~46, 다시 안 돌림)
#   GR : --sampling greedy (Q17 (a) 짧은 확인), 6과제 x 2회, 접두사 x3gr. 대조 = x3s1c 1 · 2회차. MTP 초안 수는 엔진 로그에서 센다
# 설정 고정 · 슬롯 확인 · nvidia-smi 는 h2k-chain 과 같다. 끝나면 서버 종료 · 밤 모드(user-mode). 끝 표시 '[nrg] done'.
param([int]$Context = 32768, [int]$RtReps = 5, [int]$GrReps = 2, [int]$ExpectSlots = 63)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$engLog = "C:\strata-lab\engine\strata-qwen36-ctx$Context-nrg.log"
function Slots {
  if (-not (Test-Path $engLog)) { return -1 }
  $m = Select-String -Path $engLog -Pattern 'hybrid experts: (\d+) of 256' | Select-Object -Last 1
  if ($m) { return [int]$m.Matches[0].Groups[1].Value } else { return -1 }
}
function Start-Server {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context -Tag nrg" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-nrg.log" -RedirectStandardError "C:\strata-lab\engine\serve-nrg.err" -WindowStyle Hidden
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
    "[nrg] server start try $try (GPU used before $vram MiB) $(Get-Date -Format s)"
    $h = Start-Server
    $s = Slots
    "[nrg] server loaded=$($h.loaded) slots=$s (expect $ExpectSlots)"
    if ($s -eq $ExpectSlots) { break }
    "[nrg] 경고: 슬롯 수가 다름 - 다시 띄움"
  }
  return $h
}
"[nrg] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
"[nrg] power $((powercfg /getactivescheme) -join ' ')"
if (Get-Process llama-quantize, llama-imatrix, llama-perplexity -ErrorAction SilentlyContinue) { "[nrg] 다른 llama 작업이 떠 있음 - 중단"; "[nrg] done $(Get-Date -Format s)"; exit 1 }
$gpu = Start-Process nvidia-smi -ArgumentList '--query-gpu=timestamp,temperature.gpu,clocks.sm,clocks.mem,power.draw,memory.used,clocks_event_reasons.active --format=csv -l 60 -f C:\strata-lab\engine\gpu-nrg.csv' -WindowStyle Hidden -PassThru
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$h = Ensure-Server
"[nrg] ready ctx $($h.max_context) $(Get-Date -Format s)"
$tasks = @('dg_group_names', 'marker_extras', 'version_bump', 'tags_platform_filter', 'metadata_extra_dupes', 'specifier_bounds')
$hb = @('--harness', 'H0', '--tool-out', 'chars', '--reasoning-echo', 'none', '--final-turn', 'none', '--seed-per-rep')
$plan = @()
for ($r = 1; $r -le $RtReps; $r++) { $plan += @{n = 'RT'; x = 'x3rt'; r = $r; a = $hb + @('--sampling', 'card-coding', '--run-tests', 'on')} }
for ($r = 1; $r -le $GrReps; $r++) { $plan += @{n = 'GR'; x = 'x3gr'; r = $r; a = $hb + @('--sampling', 'greedy')} }
foreach ($p in $plan) {
  $null = Ensure-Server
  $extra = $p.a
  "[nrg] rep $($p.r) $($p.n) $(Get-Date -Format s)"
  & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks @tasks --prefix $p.x @extra --rep-start $p.r 2>&1 | ForEach-Object { "[nrg] $_" }
  "[nrg] rep $($p.r) $($p.n) end $(Get-Date -Format s)"
}
if (Test-Path $engLog) {
  $d = Select-String -Path $engLog -Pattern 'drafts accepted (\d+) of (\d+)'
  $acc = ($d | ForEach-Object { [int]$_.Matches[0].Groups[1].Value } | Measure-Object -Sum).Sum
  $off = ($d | ForEach-Object { [int]$_.Matches[0].Groups[2].Value } | Measure-Object -Sum).Sum
  "[nrg] engine drafts: requests $(@($d).Count), accepted $acc of $off"
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
if ($gpu -and -not $gpu.HasExited) { Stop-Process -Id $gpu.Id -Force }
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1 | ForEach-Object { "[nrg] $_" }
"[nrg] done $(Get-Date -Format s)"
