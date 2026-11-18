# B1-1: thinking 상한 비교 (T-007 · Q12). M0 · E0 · H0 고정, 32K, max_tokens 8,192, 짧은 입력, 탐색 과제 5개(kv_store = 긴 답변).
# S0 = 예산 없음(서버 answer_room → 6,144), S1T3/S1T4/S1T6 = 요청의 reasoning_budget_tokens 3,072 / 4,608 / 6,144.
param([int]$Context = 32768, [int]$Budget = 8192, [int]$Repeat = 3, [string]$Prefix = 'b1',
      [string[]]$Cells = @('S1T3:3072', 'S1T4:4608', 'S1T6:6144', 'S0:0'))
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$k = [int]($Context / 1024)
"[b1] start server ctx $Context $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\cleanup.ps1 | Select-Object -Last 1
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
  -RedirectStandardOutput "C:\strata-lab\engine\serve-b1-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-b1-ctx${k}k.err" -WindowStyle Hidden
$h = $null
for ($i = 0; $i -lt 120; $i++) {
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
  Start-Sleep -Seconds 5
}
"[b1] ready ctx $($h.max_context) $(Get-Date -Format s)"
foreach ($c in $Cells) {
  $sid, $rbt = $c -split ':'
  "[b1] cell $sid reasoning_budget $rbt $(Get-Date -Format s)"
  & $py C:\strata-lab\scripts\bench\run_coding.py --ctx $Context --budgets $Budget --repeat $Repeat --prefix $Prefix `
    --config-id B1 --settings-id $sid --reasoning-budget $rbt 2>&1 | ForEach-Object { "[b1] $_" }
}
"[b1] done $(Get-Date -Format s)"
