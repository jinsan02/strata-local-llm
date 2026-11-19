# 64K 속도 곡선 보강 (11-19 사용자 요청): 64K 서버에서 입력 32K · 40K (출력 512, 워밍업 1 + 3회).
# 11-19 ctx64 체인의 24K(53 tok/s) · 48K(24.5 tok/s) 사이가 비어 있어, 배분안(작업 공간 문턱 약 36K)의 근거를 채운다.
# 매 측정 뒤 남은 RAM · 페이지 파일 사용량을 남긴다(48K 급락이 페이지 파일 때문인지 가르는 단서). 끝 표시 '[k64c] done'.
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$eng = 'C:\strata-lab\engine'
$ctx = 65536
function Mem([string]$at) {
  $o = Get-CimInstance Win32_OperatingSystem
  $pf = (Get-CimInstance Win32_PageFileUsage | Select-Object -First 1).CurrentUsage
  "[k64c] mem $at | free RAM $([math]::Round($o.FreePhysicalMemory / 1MB, 2))GB commit free $([math]::Round($o.FreeVirtualMemory / 1MB, 2))GB pagefile used ${pf}MB"
}
"[k64c] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $ctx -Tag k64c" `
  -RedirectStandardOutput "$eng\serve-k64c.log" -RedirectStandardError "$eng\serve-k64c.err" -WindowStyle Hidden
$h = $null
for ($i = 0; $i -lt 120; $i++) {
  Start-Sleep -Seconds 5
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $ctx -and $h.loaded) { break } } catch {}
}
$slots = Select-String -Path "$eng\strata-qwen36-ctx$ctx-k64c.log" -Pattern 'hybrid experts' -ErrorAction SilentlyContinue | Select-Object -Last 1 | ForEach-Object { $_.Line }
"[k64c] ready=$($h.loaded) $(Get-Date -Format s) | $slots"
Mem 'after start'
if ($h -and $h.loaded) {
  foreach ($n in 32768, 40960) {
    $k = [int]($n / 1024)
    & $py -u C:\strata-lab\scripts\bench\run_bench.py --run-id "k64_m0_e0_s0_ctx64k_curve_in${k}k" --config-id X64 --phase config `
      --workload "ctx64-in${k}k" --target-tokens $n --max-tokens 512 --repeat 3 --warmup 1 --ctx $ctx --note "64K 곡선 보강: ctx $ctx, 입력 $n" 2>&1 | ForEach-Object { "[k64c] $_" }
    Mem "after in${k}k"
  }
} else { "[k64c] 서버가 뜨지 않음 - 건너뜀" }
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
"[k64c] done $(Get-Date -Format s)"
