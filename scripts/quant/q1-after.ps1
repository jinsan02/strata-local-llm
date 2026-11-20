# Q1 밤 체인 뒤 이어 돌기 (11-20 사용자: 공개 보정 자료 둘 다 받아 imatrix 비교 추가). 서버 없이.
#   (1) R0u = R0 레시피 + Unsloth imatrix(M0 를 만든 것) -> 우리 도구 체인이 M0 를 재현하는지 확인용
#   (2) bartowski calibration-v6 를 Qwen3.6 템플릿으로 렌더링해 우리 보정 세트와 섞고 imatrix-mix 계산(--parse-special)
# q1-night 의 '[q1] done' 을 기다림. 로그는 호출 쪽에서 engine\q1-after.log 로, 끝 표시 '[q1b] done'. 커밋 없음.
param([int]$Threads = 12, [int]$Chunks = 600)
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'; $W = "$R\work\q1"; $B = "$R\work\llama.cpp\build\bin"; $e = "$R\engine"
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$bf = "$R\data\models\qwen36-bf16\Qwen3.6-35B-A3B-BF16-00001-of-00002.gguf"
$q8 = "$R\data\models\qwen36-q8_0\Qwen3.6-35B-A3B-Q8_0.gguf"
$uimat = "$R\data\calib\imatrix_unsloth.gguf"
function Stamp { Get-Date -Format s }
"[q1b] wait $(Stamp)"
for ($i = 0; $i -lt 900; $i++) {
  if ((Test-Path "$e\q1-night.log") -and (Select-String -Path "$e\q1-night.log" -Pattern '\[q1\] done' -Quiet)) { break }
  Start-Sleep -Seconds 60
}
if (-not (Select-String -Path "$e\q1-night.log" -Pattern '\[q1\] done' -Quiet)) { "[q1b] q1-night 가 끝나지 않음 - 중단"; exit 1 }
Start-Sleep 10
if (Get-Process strata, llama-quantize, llama-imatrix -ErrorAction SilentlyContinue) { "[q1b] 서버 또는 다른 변환이 떠 있음 - 중단"; "[q1b] done $(Stamp)"; exit 1 }
if ((Get-FileHash $uimat -Algorithm SHA256).Hash.ToLower() -ne 'a96ef6a7ef174fc43cca013f4452756877e5993f6a17eec1907900e9a0608586') { "[q1b] Unsloth imatrix 해시 다름 - 중단"; "[q1b] done $(Stamp)"; exit 1 }

# (1) R0u
$out = "$R\data\models\qwen36-r0u\Qwen3.6-35B-A3B-R0U.gguf"
New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
if (-not (Test-Path $out)) {
  "[q1b] r0u start $(Stamp)"
  $t0 = Get-Date
  & "$B\llama-quantize.exe" --imatrix $uimat --tensor-type-file "$R\configs\quant\r0.txt" $bf $out Q8_0 $Threads *> "$W\r0u.log"
  $rc = $LASTEXITCODE
  "[q1b] r0u exit $rc $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, $([math]::Round((Get-Item $out -ErrorAction SilentlyContinue).Length/1GB,2)) GB"
  if (-not $rc) {
    & $py "$R\engine\tools\quant_formats.py" $out *> "$W\r0u-formats.md"
    "[q1b] r0u G0 $((Get-Content "$W\r0u-formats.md" | Select-String 'Routed experts:') -join ' ') sha256 $((Get-FileHash $out -Algorithm SHA256).Hash.ToLower())"
    # M0 와 텐서별 형식 대조(expert 포함) - 같아야 재현이 맞다
    & $py "$R\scripts\quant\gguf_types_diff.py" "$R\data\models\qwen36-ud-q4_k_xl\Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf" $out 2>&1 | ForEach-Object { "[q1b]   M0 vs R0u: $_" }
  } else { Get-Content "$W\r0u.log" -Tail 5 | ForEach-Object { "[q1b]   $_" }; "[q1b] 경고: r0u 실패" }
}

# (2) V6 렌더링 + 섞기 + imatrix-mix
"[q1b] render $(Stamp)"
& $py "$R\scripts\quant\render_v6.py" --ours "$W\calib.txt" --out-v6 "$W\calib-v6.txt" --out-mix "$W\calib-mix.txt" 2>&1 | ForEach-Object { "[q1b]   $_" }
if (-not (Test-Path "$W\calib-mix.txt")) { "[q1b] 오류: 섞은 보정 세트 없음 - 중단"; "[q1b] done $(Stamp)"; exit 1 }
$imix = "$W\imatrix-mix.gguf"
if (-not (Test-Path $imix)) {
  "[q1b] imatrix-mix start $(Stamp)"
  $t0 = Get-Date
  & "$B\llama-imatrix.exe" -m $q8 -f "$W\calib-mix.txt" -o $imix -c 512 --chunks $Chunks -ngl 99 -ot 'ffn_.*_exps=CPU' -t $Threads --parse-special *> "$W\imatrix-mix.log"
  "[q1b] imatrix-mix exit $LASTEXITCODE $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min"
  Get-Content "$W\imatrix-mix.log" -Tail 3 | ForEach-Object { "[q1b]   $_" }
}
"[q1b] done $(Stamp)"
