# 밤 체인(노트북 연결과 무관하게 본체에서만 돈다): WMI 로 띄워 ssh 세션이 끝나도 살아 있다.
# 1) 서버 32K 기동  2) 캐시 재사용 점검 다시(2회)  3) H0 · H1 을 번갈아 3회 (X3 navigate 3과제 + SWE 2건)  4) 서버 종료 · 밤 모드
# 끝 표시: engine\night-chain.log 의 '[night] done'. 원장 커밋은 하지 않는다(연결 재개 후 Claude 가 확인하고 커밋).
param([int]$Context = 32768, [int]$Reps = 3)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
function Ensure-Server {
  $h = $null
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if ($h -and $h.loaded -and $h.max_context -eq $Context) { return $h }
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
  $k = [int]($Context / 1024)
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-night-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-night-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  return $h
}
"[night] start $(Get-Date -Format s)"
$h = Ensure-Server
"[night] ready ctx $($h.max_context) $(Get-Date -Format s)"
New-Item -ItemType Directory -Force C:\strata-lab\experiments\probes | Out-Null
Set-Location C:\strata-lab\experiments\probes
& $py -u C:\strata-lab\scripts\bench\probe_cache.py --repeat 2 --out probe_cache_20261118.json 2>&1 | ForEach-Object { "[night] $_" }
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in @(@{h='H0'; t='chars'}, @{h='H1'; t='paged'})) {
    $null = Ensure-Server
    $x = 'x3' + $arm.h.ToLower(); $s = 'x3s' + $arm.h.ToLower()
    "[night] rep $r $($arm.h) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix $x --harness $arm.h --tool-out $arm.t --rep-start $r 2>&1 | ForEach-Object { "[night] $_" }
    & $py -u C:\strata-lab\scripts\bench\run_swe.py --prefix $s --harness $arm.h --tool-out $arm.t --rep-start $r 2>&1 | ForEach-Object { "[night] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[night] done $(Get-Date -Format s)"
