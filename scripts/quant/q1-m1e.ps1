# 11-21 M1e (docs/engine-kernels-20261121.md 5절): M1b 의 down IQ4_XS -> IQ4_NL. 엔진 fused 커널 짝(IQ4_XS gate/up + IQ4_NL down)이 되는지 확인.
# 순서: 생성(I-ours) -> M1b 와 형식 비교 -> G2 KL(같은 기준 로짓) -> 서버 적재 · 커널 경로 · PP(M0 와 같은 탐침, g3-chain -Reps 0). 끝 표시 '[m1e] done'.
param([int]$Threads = 12)
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'; $W = "$R\work\q1"; $B = "$R\work\llama.cpp\build\bin"; $D = "$R\data\models"
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$bf = "$D\qwen36-bf16\Qwen3.6-35B-A3B-BF16-00001-of-00002.gguf"
$out = "$D\qwen36-m1e\Qwen3.6-35B-A3B-M1E.gguf"
"[m1e] start $(Get-Date -Format s) commit $(git -C $R rev-parse --short HEAD)"
if (Get-Process strata, llama-quantize, llama-imatrix, llama-perplexity -ErrorAction SilentlyContinue) { "[m1e] 서버 또는 다른 llama 작업이 떠 있음 - 중단"; "[m1e] done $(Get-Date -Format s)"; exit 1 }
New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
if (-not (Test-Path $out)) {
  $t0 = Get-Date
  & "$B\llama-quantize.exe" --imatrix "$W\imatrix-coding.gguf" --tensor-type-file "$R\configs\quant\m1e.txt" $bf $out Q8_0 $Threads *> "$W\m1e.log"
  $rc = $LASTEXITCODE
  "[m1e] quantize exit $rc $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, $([math]::Round((Get-Item $out -ErrorAction SilentlyContinue).Length/1GB,2)) GB"
  if ($rc) { Get-Content "$W\m1e.log" -Tail 5 | ForEach-Object { "[m1e]   $_" }; "[m1e] 오류: 생성 실패"; "[m1e] done $(Get-Date -Format s)"; exit 1 }
}
& $py "$R\scripts\quant\gguf_types_diff.py" "$D\qwen36-m1b\Qwen3.6-35B-A3B-M1B.gguf" $out 2>&1 | ForEach-Object { "[m1e]   M1b vs M1e: $_" }
"[m1e] G0 sha256 $((Get-FileHash $out -Algorithm SHA256).Hash.ToLower())"
"[m1e] kl $(Get-Date -Format s)"
& "$R\scripts\quant\q1-g2.ps1" -Only @('M1e') -Threads $Threads 2>&1 | ForEach-Object { "[m1e] $_" }
"[m1e] load+pp $(Get-Date -Format s)"
& "$R\scripts\bench\g3-chain.ps1" -Only @('M0', 'M1e') -Reps 0 2>&1 | ForEach-Object { "[m1e] $_" }
"[m1e] done $(Get-Date -Format s)"
