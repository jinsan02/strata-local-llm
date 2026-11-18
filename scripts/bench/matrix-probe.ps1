# 하네스 점검: 서버 32K 가 없으면 낮 모드 후 기동 -> 도구 왕복(probe_tools) -> 캐시 재사용(probe_cache) -> (선택) navigate H0 기준선.
# 서버는 이 스크립트를 띄운 ssh 세션이 끝나면 같이 종료되므로(11-18 확인) 측정은 한 세션 안에서 한다.
param([int]$Context = 32768, [switch]$Baseline, [string]$Out = 'C:\strata-lab\experiments\probes')
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
New-Item -ItemType Directory -Force $Out | Out-Null
$h = $null
try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
if (-not ($h -and $h.loaded -and $h.max_context -eq $Context)) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
  $k = [int]($Context / 1024)
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-probe-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-probe-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
}
"[probe] ready ctx $($h.max_context) $(Get-Date -Format s)"
Set-Location $Out
& $py -u C:\strata-lab\scripts\bench\probe_tools.py --repeat 2 --out probe_tools_20261118.json 2>&1 | ForEach-Object { "[probe] $_" }
& $py -u C:\strata-lab\scripts\bench\probe_cache.py --out probe_cache_20261118.json 2>&1 | ForEach-Object { "[probe] $_" }
if ($Baseline) {
  & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix x3h0 --harness H0 2>&1 | ForEach-Object { "[probe] $_" }
  & $py -u C:\strata-lab\scripts\bench\run_swe.py --prefix x3sh0 --harness H0 2>&1 | ForEach-Object { "[probe] $_" }
}
"[probe] done $(Get-Date -Format s)"
