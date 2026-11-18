# T-011 재측정: navigate v2(edit_file + 텍스트 도구 호출 1회 재요청)로 X3 3과제 + SWE 2건. 서버 32K 가 없으면 낮 모드 후 기동.
param([int]$Context = 32768, [string]$X3Prefix = 'x3n', [string]$SwePrefix = 'x3sn')
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$h = $null
try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
if (-not ($h -and $h.loaded -and $h.max_context -eq $Context)) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
  $k = [int]($Context / 1024)
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-nav-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-nav-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
}
"[nav] ready ctx $($h.max_context) $(Get-Date -Format s)"
& $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix $X3Prefix 2>&1 | ForEach-Object { "[nav] $_" }
& $py -u C:\strata-lab\scripts\bench\run_swe.py --prefix $SwePrefix 2>&1 | ForEach-Object { "[nav] $_" }
"[nav] done $(Get-Date -Format s)"
