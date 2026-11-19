# B1 P-diag 1단계 (v2.2 10.2 · 10.3 '기존 설정부터'): VRAM 상주 expert 슬롯 수가 decode · prefill 에 주는 영향.
# 32K 고정, 실제 입력 8K · 24K, 출력 512, 워밍업 1 + 3회, 같은 세션에서 조건마다 서버를 새로 띄운다. 프로파일러 없이(Nsight 미설치).
#   base     : 기본 (63 슬롯)
#   slots40  : --expert-slots 40 (곡선의 아래 점)
#   evram69  : --expert-vram 6.2 (예약 768MiB → 약 300MiB, 약 69 슬롯 예상)
#   nopf     : STRATA_Q36_NO_MMQ=1 · STRATA_EXPERT_I8=0 (흘려 읽는 prefill 경로를 끄면 staging 1.10GiB 가 슬롯으로, 약 78 예상. prefill 은 느려질 수 있음)
#   base2    : 기본 다시 (드리프트 확인)
# 슬롯 수는 엔진 로그 'hybrid experts' 줄로 확인한다. 끝 표시 '[pdiag] done'. 원장 커밋은 Claude 가 대조 뒤.
param([int]$Context = 32768, [int]$Repeat = 3)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$eng = 'C:\strata-lab\engine'
$conds = @(
  @{t = 'base';    x = '';                     e = ''},
  @{t = 'slots40'; x = '--expert-slots 40';    e = ''},
  @{t = 'evram69'; x = '--expert-vram 6.2';    e = ''},
  @{t = 'nopf';    x = '';                     e = 'STRATA_Q36_NO_MMQ=1;STRATA_EXPERT_I8=0'},
  @{t = 'base2';   x = '';                     e = ''}
)
"[pdiag] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
foreach ($c in $conds) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  $elog = Join-Path $eng "strata-qwen36-ctx$Context-pd1$($c.t).log"
  $args1 = "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context -Tag pd1$($c.t)"
  if ($c.x) { $args1 += " -ExtraArgs `"$($c.x)`"" }
  if ($c.e) { $args1 += " -EnvSet `"$($c.e)`"" }
  Start-Process powershell -ArgumentList $args1 -RedirectStandardOutput "$eng\serve-pd1-$($c.t).log" -RedirectStandardError "$eng\serve-pd1-$($c.t).err" -WindowStyle Hidden
  $h = $null
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  $slots = (Select-String -Path $elog -Pattern 'hybrid experts|VRAM free|not enough VRAM' -ErrorAction SilentlyContinue | Select-Object -Last 2 | ForEach-Object { $_.Line }) -join ' || '
  "[pdiag] $($c.t) ready=$($h.loaded) $(Get-Date -Format s) | $slots"
  if (-not $h.loaded) { "[pdiag] $($c.t) 서버가 뜨지 않음 - 건너뜀"; continue }
  foreach ($n in 8192, 24320) {
    $k = [int]($n / 1024)
    & $py -u C:\strata-lab\scripts\bench\run_bench.py --run-id "pd1_m0_e0_s0_ctx32k_$($c.t)_in${k}k" --config-id B1-PD1 --phase config `
      --workload "pdiag-decode-in${k}k" --target-tokens $n --max-tokens 512 --repeat $Repeat --warmup 1 --ctx $Context `
      --note "P-diag 1: $($c.t) [$($c.x)$($c.e)] | $slots" 2>&1 | ForEach-Object { "[pdiag] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[pdiag] done $(Get-Date -Format s)"
