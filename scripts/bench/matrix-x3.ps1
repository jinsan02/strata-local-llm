# X3 파일럿: B1-1 이 끝나기를 기다린 뒤 (GPU 측정 겹치지 않게) 낮 모드 정리 → 서버 새로 기동 → preload 9회 → navigate 3회.
# preload 입력: 0 = 필수 파일만(dg 약 8K, marker · version 약 12K), 16,384, 24,320. 출력+reasoning 8,192, 서버 32K, S0.
param([int]$Context = 32768, [string]$WaitLog = 'C:\strata-lab\engine\matrix-b1t.log', [string]$Prefix = 'x3p')
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
"[x3] waiting for B1 $(Get-Date -Format s)"
# 끝 표시만 믿는다 (셀 사이에 run_coding 프로세스가 잠깐 없어서 프로세스 검사는 오판할 수 있다). 최대 4시간.
$deadline = (Get-Date).AddHours(4)
while ((Get-Date) -lt $deadline) {
  if ((Test-Path $WaitLog) -and (Select-String -Path $WaitLog -Pattern '\[b1\] done' -Quiet)) { break }
  Start-Sleep -Seconds 30
}
if (-not (Select-String -Path $WaitLog -Pattern '\[b1\] done' -Quiet)) { "[x3] B1 done marker not seen in 4h, stop"; exit 1 }
"[x3] B1 finished $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$k = [int]($Context / 1024)
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
  -RedirectStandardOutput "C:\strata-lab\engine\serve-x3-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-x3-ctx${k}k.err" -WindowStyle Hidden
$h = $null
for ($i = 0; $i -lt 120; $i++) {
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
  Start-Sleep -Seconds 5
}
"[x3] ready ctx $($h.max_context) $(Get-Date -Format s)"
& $py -u C:\strata-lab\scripts\bench\run_x3.py --mode preload --inputs 0 16384 24320 --prefix $Prefix 2>&1 | ForEach-Object { "[x3] $_" }
"[x3] preload done $(Get-Date -Format s)"
& $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix $Prefix 2>&1 | ForEach-Object { "[x3] $_" }
"[x3] done $(Get-Date -Format s)"
