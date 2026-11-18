# B0 + X1 매트릭스: 같은 M0 · E0 · S0 · 샘플링에서 컨텍스트 설정만 바꾼다 (입력 길이는 고정 문항).
# 컨텍스트마다 서버를 다시 띄우고, 입력 512 · 2048 · 4096 × 출력 128 · 512 를 반복 3회(예열 1회) 잰다.
# 8K 행은 B0(기준선)을 겸한다. 진행 상황은 한 줄씩 출력한다.
param([int[]]$Contexts = @(32768, 16384, 8192), [int[]]$Inputs = @(512, 2048, 4096), [int[]]$Outputs = @(128, 512), [int]$Repeat = 3)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
function Wait-Ready([int]$ctx) {
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $ctx -and $h.loaded) { return $true } } catch {}
    Start-Sleep -Seconds 5
  }
  return $false
}
foreach ($ctx in $Contexts) {
  $k = [int]($ctx / 1024)
  "[x1] ctx ${ctx}: server $(Get-Date -Format s)"
  $h = $null; try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if (-not $h -or $h.max_context -ne $ctx) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
    & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\cleanup.ps1 | Select-Object -Last 1
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $ctx" `
      -RedirectStandardOutput "C:\strata-lab\engine\serve-x1-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-x1-ctx${k}k.err" -WindowStyle Hidden
    if (-not (Wait-Ready $ctx)) { "[x1] ctx ${ctx}: server did not become ready (fail)"; continue }
  }
  "[x1] ctx ${ctx}: ready $(Get-Date -Format s)"
  foreach ($in in $Inputs) { foreach ($out in $Outputs) {
    $cfg = if ($ctx -eq 8192) { 'B0' } else { 'X1' }
    $rid = "x1_m0_e0_s0_ctx${k}k_in${in}_out${out}"
    $res = & $py C:\strata-lab\scripts\bench\run_bench.py --run-id $rid --config-id $cfg --ctx $ctx --workload "fixed-$in" `
             --target-tokens $in --max-tokens $out --repeat $Repeat --warmup 1 2>&1
    $res | ForEach-Object { "[x1] $_" }
  } }
}
"[x1] done $(Get-Date -Format s)"
