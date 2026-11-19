# 64K 도입 점검 (Q16, v2.2 10.6 앞당김): 설정 효과와 코딩 효과를 나눠 잰다. 같은 세션, 서버는 조건마다 새로 띄운다.
#  1) 설정 효과: 32K vs 64K 설정에서 같은 24K 입력(출력 512, 워밍업 1 + 3회) → TG · PP · 슬롯 · VRAM · RAM
#  2) 긴 입력: 64K 설정에서 실제 48K 입력 → prefill 시간 · 첫 스트림 · 메모리 부족 여부
#  3) 코딩 효과: X3 navigate 3과제, 하네스는 기준 H0(11-19 채택 확인에서 H3 기각), 32K vs 64K 번갈아 3회.
#     64K 의 강제 턴 문턱은 ctx - budget - 2048 = 55,296(32K 는 22,272). 출력 예산 8,192 는 같게(변수 하나).
# 슬롯 · VRAM 은 엔진 로그 'hybrid experts' · 'VRAM free' 줄. 끝 표시 '[ctx64] done'. 원장 커밋은 Claude 가 대조 뒤.
param([int]$Reps = 3)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$eng = 'C:\strata-lab\engine'
function Start-Ctx([int]$ctx) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $ctx" `
    -RedirectStandardOutput "$eng\serve-ctx64chain-$ctx.log" -RedirectStandardError "$eng\serve-ctx64chain-$ctx.err" -WindowStyle Hidden
  $h = $null
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $ctx -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  $elog = Join-Path $eng "strata-qwen36-ctx$ctx.log"
  $lines = (Select-String -Path $elog -Pattern 'hybrid experts|VRAM free|not enough VRAM' -ErrorAction SilentlyContinue | Select-Object -Last 2 | ForEach-Object { $_.Line }) -join ' || '
  $o = Get-CimInstance Win32_OperatingSystem
  $pf = (Get-CimInstance Win32_PageFileUsage | Select-Object -First 1).CurrentUsage
  # Write-Host: 함수 반환값($h)에 섞이지 않게(체인 로그는 *>&1 로 함께 남는다)
  Write-Host "[ctx64] ctx $ctx ready=$($h.loaded) $(Get-Date -Format s) | free RAM $([math]::Round($o.FreePhysicalMemory / 1MB, 2))GB commit free $([math]::Round($o.FreeVirtualMemory / 1MB, 2))GB pagefile used ${pf}MB | $lines"
  return $h
}
function Bench([int]$ctx, [int]$n, [string]$tag) {
  $k = [int]($n / 1024)
  & $py -u C:\strata-lab\scripts\bench\run_bench.py --run-id "k64_m0_e0_s0_ctx$([int]($ctx / 1024))k_${tag}_in${k}k" --config-id X64 --phase config `
    --workload "ctx64-in${k}k" --target-tokens $n --max-tokens 512 --repeat 3 --warmup 1 --ctx $ctx --note "64K 점검: ctx $ctx, 입력 $n" 2>&1 | ForEach-Object { "[ctx64] $_" }
}
"[ctx64] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
# 1 · 2) 설정 효과 · 긴 입력
if ((Start-Ctx 32768).loaded) { Bench 32768 24320 'set' }
if ((Start-Ctx 65536).loaded) { Bench 65536 24320 'set'; Bench 65536 49152 'long' }
# 3) 코딩 효과 (H0, 32K vs 64K 번갈아)
$hb = @('--harness', 'H0', '--tool-out', 'chars', '--reasoning-echo', 'none', '--final-turn', 'none')
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($ctx in 32768, 65536) {
    $h = Start-Ctx $ctx
    if (-not $h.loaded) { "[ctx64] ctx $ctx 서버가 뜨지 않음 - 건너뜀"; continue }
    "[ctx64] rep $r ctx $ctx $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --ctx $ctx --prefix "x3k$([int]($ctx / 1024))h0" @hb --rep-start $r 2>&1 | ForEach-Object { "[ctx64] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[ctx64] done $(Get-Date -Format s)"
