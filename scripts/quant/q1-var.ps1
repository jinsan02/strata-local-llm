# Q1 imatrix 비교(q1-plan 10절): G2 를 통과한 M1a · M1b 를 I-unsloth(-u) · I-mix(-x) 로 다시 만들고, 같은 기준 로짓으로 KL 을 잰다.
# I-ours 판은 이미 있다(M1a · M1b). 서버 없이. 로그는 호출 쪽에서 engine\q1-var.log, 끝 표시 '[var] done'. 커밋 없음.
param([int]$Threads = 12)
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'; $W = "$R\work\q1"; $B = "$R\work\llama.cpp\build\bin"; $D = "$R\data\models"
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$bf = "$D\qwen36-bf16\Qwen3.6-35B-A3B-BF16-00001-of-00002.gguf"
function Stamp { Get-Date -Format s }
"[var] start $(Stamp)"
if (Get-Process strata, llama-quantize, llama-imatrix, llama-perplexity -ErrorAction SilentlyContinue) { "[var] 서버 또는 다른 llama 작업이 떠 있음 - 중단"; "[var] done $(Stamp)"; exit 1 }
$imat = @{ u = "$R\data\calib\imatrix_unsloth.gguf"; x = "$W\imatrix-mix.gguf" }
if ((Get-FileHash $imat.u -Algorithm SHA256).Hash.ToLower() -ne 'a96ef6a7ef174fc43cca013f4452756877e5993f6a17eec1907900e9a0608586') { "[var] 오류: Unsloth imatrix 해시 다름 - 중단"; "[var] done $(Stamp)"; exit 1 }
"[var] imatrix-mix sha256 $((Get-FileHash $imat.x -Algorithm SHA256).Hash.ToLower())"
$built = @()
foreach ($c in 'm1a', 'm1b') {
  foreach ($k in 'u', 'x') {
    $n = "$c-$k"; $out = "$D\qwen36-$n\Qwen3.6-35B-A3B-$($n.ToUpper()).gguf"
    New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
    if (-not (Test-Path $out)) {
      $t0 = Get-Date
      & "$B\llama-quantize.exe" --imatrix $imat[$k] --tensor-type-file "$R\configs\quant\$c.txt" $bf $out Q8_0 $Threads *> "$W\$n.log"
      $rc = $LASTEXITCODE
      "[var] $n exit $rc $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, $([math]::Round((Get-Item $out -ErrorAction SilentlyContinue).Length/1GB,2)) GB"
      if ($rc) { Get-Content "$W\$n.log" -Tail 5 | ForEach-Object { "[var]   $_" }; "[var] 경고: $n 실패"; continue }
    }
    # 같은 레시피의 I-ours 판과 텐서 형식이 같아야 한다(imatrix 만 다름)
    & $py "$R\scripts\quant\gguf_types_diff.py" "$D\qwen36-$c\Qwen3.6-35B-A3B-$($c.ToUpper()).gguf" $out 2>&1 | ForEach-Object { "[var]   $c vs $n`: $_" }
    "[var] $n G0 sha256 $((Get-FileHash $out -Algorithm SHA256).Hash.ToLower())"
    $built += ($c.Substring(0,1).ToUpper() + $c.Substring(1) + "-$k")
  }
}
"[var] kl $(Stamp)"
& "$R\scripts\quant\q1-g2.ps1" -Only $built -Threads $Threads 2>&1 | ForEach-Object { "[var] $_" }
"[var] done $(Stamp)"
