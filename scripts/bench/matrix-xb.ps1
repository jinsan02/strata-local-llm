# XB: 출력·reasoning 예산 단계 시험 (2K → 4K → 8K), 운영 설정 32K, 탐색 코딩 과제 4개.
param([int]$Context = 32768, [int[]]$Budgets = @(2048, 4096, 8192), [int]$Repeat = 1, [string]$Prefix = 'xb')
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$h = $null; try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
if (-not $h -or $h.max_context -ne $Context) {
  "[xb] start server ctx $Context $(Get-Date -Format s)"
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\cleanup.ps1 | Select-Object -Last 1
  $k = [int]($Context / 1024)
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-xb-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-xb-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
}
"[xb] ready ctx $($h.max_context) $(Get-Date -Format s)"
& $py C:\strata-lab\scripts\bench\run_coding.py --ctx $Context --budgets $Budgets --repeat $Repeat --prefix $Prefix 2>&1 | ForEach-Object { "[xb] $_" }
"[xb] done $(Get-Date -Format s)"
