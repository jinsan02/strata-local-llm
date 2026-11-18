# X2: 입력 길이 효과. 운영 설정 32K 고정, 출력+reasoning 예산 8,192 (XB 결론), 탐색 코딩 과제 4개.
# 저장소 파일을 붙여 실제 입력을 약 2K · 8K · 16K · 한도 근처(32,768 - 8,192 - 256)로 늘리고, 과제 위치는 끝 · 중간.
# 서버는 매번 새로 띄운다 (정리 스크립트 → serve-ctx). 반복 2회차부터는 prefix 캐시가 맞을 수 있어 cache_state=warm 으로 남는다.
param([int]$Context = 32768, [int]$Budget = 8192, [int]$Repeat = 3, [string]$Prefix = 'x2',
      [string[]]$Cells = @('2048:end', '8192:end', '8192:middle', '16384:end', '16384:middle', '24320:end', '24320:middle'))
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$k = [int]($Context / 1024)
"[x2] start server ctx $Context $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\cleanup.ps1 | Select-Object -Last 1
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
  -RedirectStandardOutput "C:\strata-lab\engine\serve-x2-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-x2-ctx${k}k.err" -WindowStyle Hidden
$h = $null
for ($i = 0; $i -lt 120; $i++) {
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
  Start-Sleep -Seconds 5
}
"[x2] ready ctx $($h.max_context) $(Get-Date -Format s)"
foreach ($c in $Cells) {
  $n, $pos = $c -split ':'
  "[x2] cell input $n position $pos $(Get-Date -Format s)"
  & $py C:\strata-lab\scripts\bench\run_coding.py --ctx $Context --budgets $Budget --repeat $Repeat --prefix $Prefix `
    --config-id X2 --input-tokens $n --position $pos 2>&1 | ForEach-Object { "[x2] $_" }
}
"[x2] done $(Get-Date -Format s)"
