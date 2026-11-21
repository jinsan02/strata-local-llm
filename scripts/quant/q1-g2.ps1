# Q1 G2: llama.cpp KL 비교(서버 없이). 기준 = 우리 Q8_0, 세트 = work\q1\kl.txt(보정과 겹치지 않는 묶음, build_calib.py).
# 비교: 기본 M0 · R0 · R0u · M1a~M1d, -Only 로 골라 돌린다(같은 기준 로짓 재사용). 결과 줄은 '[g2] <후보> ...', 끝 표시 '[g2] done'. 커밋 없음.
# 주의: llama-perplexity 는 특수 토큰을 글자로 토큰화한다(--parse-special 없음) - 모든 후보에 같게 적용되는 상대 비교.
param([int]$Threads = 12, [int]$Ctx = 2048, [int]$Chunks = -1, [string]$Tag = '', [string[]]$Only = @())
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'; $W = "$R\work\q1"; $B = "$R\work\llama.cpp\build\bin"; $D = "$R\data\models"
function Stamp { Get-Date -Format s }
function Mem { $o = Get-CimInstance Win32_OperatingSystem; $pf = (Get-CimInstance Win32_PageFileUsage | Measure-Object CurrentUsage -Sum).Sum
  "mem free $([math]::Round($o.FreePhysicalMemory/1MB,1)) GB, commit $([math]::Round(($o.TotalVirtualMemorySize-$o.FreeVirtualMemory)/1MB,1)) GB, pagefile $pf MB" }
"[g2] start $(Stamp) ctx $Ctx chunks $Chunks $(Mem)"
if (Get-Process strata, llama-quantize, llama-imatrix, llama-perplexity -ErrorAction SilentlyContinue) { "[g2] 서버 또는 다른 llama 작업이 떠 있음 - 중단"; "[g2] done $(Stamp)"; exit 1 }
$q8 = "$D\qwen36-q8_0\Qwen3.6-35B-A3B-Q8_0.gguf"
$base = "$W\kl-base-c$Ctx$Tag.bin"
$common = @('-f', "$W\kl.txt", '-c', $Ctx, '--chunks', $Chunks, '-ngl', '99', '-ot', 'ffn_.*_exps=CPU', '-t', $Threads)
if (-not (Test-Path $base)) {
  $t0 = Get-Date
  & "$B\llama-perplexity.exe" -m $q8 --kl-divergence-base $base @common *> "$W\kl-base$Tag.log"
  $rc = $LASTEXITCODE
  "[g2] base exit $rc $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, $([math]::Round((Get-Item $base -ErrorAction SilentlyContinue).Length/1GB,2)) GB, $((Select-String -Path "$W\kl-base$Tag.log" -Pattern 'Final estimate' | Select-Object -Last 1).Line) $(Mem)"
  if ($rc) { Get-Content "$W\kl-base$Tag.log" -Tail 5 | ForEach-Object { "[g2]   $_" }; "[g2] 오류: 기준 로짓 실패 - 중단"; "[g2] done $(Stamp)"; exit 1 }
}
$models = [ordered]@{
  M0  = "$D\qwen36-ud-q4_k_xl\Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf"
  R0  = "$D\qwen36-r0\Qwen3.6-35B-A3B-R0.gguf"
  R0u = "$D\qwen36-r0u\Qwen3.6-35B-A3B-R0U.gguf"
  M1a = "$D\qwen36-m1a\Qwen3.6-35B-A3B-M1A.gguf"
  M1b = "$D\qwen36-m1b\Qwen3.6-35B-A3B-M1B.gguf"
  M1e = "$D\qwen36-m1e\Qwen3.6-35B-A3B-M1E.gguf"   # 11-21: down IQ4_NL (engine-kernels 5절)
  M1c = "$D\qwen36-m1c\Qwen3.6-35B-A3B-M1C.gguf"
  M1d = "$D\qwen36-m1d\Qwen3.6-35B-A3B-M1D.gguf"
  # imatrix 비교(10절): -u = I-unsloth, -x = I-mix. q1-var.ps1 이 만든다
  'M1a-u' = "$D\qwen36-m1a-u\Qwen3.6-35B-A3B-M1A-U.gguf"
  'M1a-x' = "$D\qwen36-m1a-x\Qwen3.6-35B-A3B-M1A-X.gguf"
  'M1b-u' = "$D\qwen36-m1b-u\Qwen3.6-35B-A3B-M1B-U.gguf"
  'M1b-x' = "$D\qwen36-m1b-x\Qwen3.6-35B-A3B-M1B-X.gguf"
}
$names = if ($Only.Count) { $Only } else { @('M0', 'R0', 'R0u', 'M1a', 'M1b', 'M1c', 'M1d') }
foreach ($n in $names) {
  $p = $models[$n]
  if (-not (Test-Path $p)) { "[g2] 경고: $n 파일 없음 $p"; continue }
  $log = "$W\kl-$n$Tag.log"
  $t0 = Get-Date
  & "$B\llama-perplexity.exe" -m $p --kl-divergence-base $base --kl-divergence @common *> $log
  $rc = $LASTEXITCODE
  $s = (Select-String -Path $log -Pattern '^(Mean +KLD|99\.0% +KLD|Same top p|Mean PPL\(Q\)/PPL\(base\)|RMS Δp)' | ForEach-Object { ($_.Line -replace '\s+', ' ').Trim() }) -join ' | '
  "[g2] $n exit $rc $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min | $s"
  if ($rc) { Get-Content $log -Tail 5 | ForEach-Object { "[g2]   $_" }; "[g2] 경고: $n 실패" }
}
"[g2] $(Mem)"
"[g2] done $(Stamp)"
