# 11-21 M2 (q1-plan 17절, 완만한 안): M0 에서 gate/up 만 Q4_K -> IQ4_XS, down 은 M0 그대로(Q5_K, 34 · 38 · 39 층 Q6_K). M1e 의 G4 하락이 down 4.5bpw 탓인지 가른다. 엔진 경로 = int8(fused 짝 아님).
# 순서: 생성(I-ours) -> M0 와 형식 비교 -> G2 KL(같은 기준 로짓) -> 서버 적재 · 커널 경로 · PP(g3-chain -Reps 0, M0 PP 는 같은 날 1,525). 끝 표시 '[m2] done'.
param([int]$Threads = 12)
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'; $W = "$R\work\q1"; $B = "$R\work\llama.cpp\build\bin"; $D = "$R\data\models"
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$bf = "$D\qwen36-bf16\Qwen3.6-35B-A3B-BF16-00001-of-00002.gguf"
$out = "$D\qwen36-m2\Qwen3.6-35B-A3B-M2.gguf"
"[m2] start $(Get-Date -Format s) commit $(git -C $R rev-parse --short HEAD)"
if (Get-Process strata, llama-quantize, llama-imatrix, llama-perplexity -ErrorAction SilentlyContinue) { "[m2] 서버 또는 다른 llama 작업이 떠 있음 - 중단"; "[m2] done $(Get-Date -Format s)"; exit 1 }
New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
if (-not (Test-Path $out)) {
  $t0 = Get-Date
  & "$B\llama-quantize.exe" --imatrix "$W\imatrix-coding.gguf" --tensor-type-file "$R\configs\quant\m2.txt" $bf $out Q8_0 $Threads *> "$W\m2.log"
  $rc = $LASTEXITCODE
  "[m2] quantize exit $rc $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, $([math]::Round((Get-Item $out -ErrorAction SilentlyContinue).Length/1GB,2)) GB"
  if ($rc) { Get-Content "$W\m2.log" -Tail 5 | ForEach-Object { "[m2]   $_" }; "[m2] 오류: 생성 실패"; "[m2] done $(Get-Date -Format s)"; exit 1 }
}
& $py "$R\scripts\quant\gguf_types_diff.py" "$D\qwen36-ud-q4_k_xl\Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf" $out 2>&1 | ForEach-Object { "[m2]   M0 vs M2: $_" }
"[m2] G0 sha256 $((Get-FileHash $out -Algorithm SHA256).Hash.ToLower())"
"[m2] kl $(Get-Date -Format s)"
& "$R\scripts\quant\q1-g2.ps1" -Only @('M2') -Threads $Threads 2>&1 | ForEach-Object { "[m2] $_" }
"[m2] load+pp $(Get-Date -Format s)"
& "$R\scripts\bench\g3-chain.ps1" -Only @('M2') -Reps 0 2>&1 | ForEach-Object { "[m2] $_" }
"[m2] done $(Get-Date -Format s)"
