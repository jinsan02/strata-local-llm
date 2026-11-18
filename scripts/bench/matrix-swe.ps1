# X3 교차 확인: X3 파일럿 끝 표시를 기다린 뒤 SWE-bench Verified 2건 환경 준비(측정 없음) -> 서버 -> 도구 탐색 풀이.
param([int]$Context = 32768, [string]$WaitLog = 'C:\strata-lab\engine\matrix-x3.log')
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
"[swe] waiting for X3 $(Get-Date -Format s)"
$deadline = (Get-Date).AddHours(6)
while ((Get-Date) -lt $deadline) {
  if ((Test-Path $WaitLog) -and (Select-String -Path $WaitLog -Pattern '\[x3\] done' -Quiet)) { break }
  Start-Sleep -Seconds 30
}
if (-not (Select-String -Path $WaitLog -Pattern '\[x3\] done' -Quiet)) { "[swe] X3 done marker not seen, stop"; exit 1 }
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
"[swe] setup $(Get-Date -Format s)"
& $py -u C:\strata-lab\scripts\bench\setup_swe.py 2>&1 | ForEach-Object { "[swe] $_" }
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$k = [int]($Context / 1024)
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
  -RedirectStandardOutput "C:\strata-lab\engine\serve-swe-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-swe-ctx${k}k.err" -WindowStyle Hidden
$h = $null
for ($i = 0; $i -lt 120; $i++) {
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
  Start-Sleep -Seconds 5
}
"[swe] ready ctx $($h.max_context) $(Get-Date -Format s)"
& $py -u C:\strata-lab\scripts\bench\run_swe.py 2>&1 | ForEach-Object { "[swe] $_" }
"[swe] done $(Get-Date -Format s)"
