# Q1 밤 체인 (docs/q1-plan-20261120.md 6절 Q1-0a ~ Q1-3, 11-20 사용자: 권장대로 진행). 서버 없이 돈다 - 변환이 RAM 을 크게 써서 측정과 겹치면 안 된다.
#   0a llama.cpp v1.0.0 CUDA 빌드(sm_120) -> 0b BF16 -> Q8_0(기준 · imatrix 용) -> 1 보정 · KL 세트 -> 2 imatrix -> 3 후보(R0 · M1a~M1d) + G0 텐서 표 · sha256
# 메모리는 15초마다 work\q1\mem.csv 에 남긴다(남은 RAM · 커밋 · 페이지 파일 · 도구 프로세스 메모리). 끝 표시 '[q1] done'. 커밋 없음.
param([string[]]$Cands = @('r0', 'm1a', 'm1b', 'm1c', 'm1d'), [int]$Threads = 12, [int]$Chunks = 400, [switch]$SkipBuild)
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'; $W = "$R\work\q1"; $L = "$R\work\llama.cpp"; $B = "$L\build\bin"
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$bf = "$R\data\models\qwen36-bf16\Qwen3.6-35B-A3B-BF16-00001-of-00002.gguf"
$q8 = "$R\data\models\qwen36-q8_0\Qwen3.6-35B-A3B-Q8_0.gguf"
$imat = "$W\imatrix-coding.gguf"
New-Item -ItemType Directory -Force $W, (Split-Path $q8) | Out-Null
function Stamp { Get-Date -Format s }
function Mem { $o = Get-CimInstance Win32_OperatingSystem; $p = Get-CimInstance Win32_PageFileUsage
  "free {0:N1} GB, commit {1:N1}/{2:N1} GB, pagefile {3} MB" -f ($o.FreePhysicalMemory/1MB), (($o.TotalVirtualMemorySize - $o.FreeVirtualMemory)/1MB), ($o.TotalVirtualMemorySize/1MB), (($p | Measure-Object CurrentUsage -Sum).Sum) }
"[q1] start $(Stamp) commit $(git -C $R rev-parse --short HEAD) llama.cpp $(git -C $L describe --tags 2>$null) $(git -C $L rev-parse --short HEAD)"
if (Get-Process strata -ErrorAction SilentlyContinue) { "[q1] 서버가 떠 있음 - 중단"; "[q1] done $(Stamp)"; exit 1 }
"[q1] mem $(Mem); disk C free $([math]::Round((Get-PSDrive C).Free/1GB)) GB"
# 메모리 기록(백그라운드 작업, 체인이 끝나면 멈춤)
$memJob = Start-Job -ArgumentList "$W\mem.csv" -ScriptBlock { param($f)
  "time,free_gb,commit_gb,pagefile_mb,tool,tool_ws_gb,tool_private_gb" | Out-File $f -Encoding utf8
  while ($true) { $o = Get-CimInstance Win32_OperatingSystem; $p = (Get-CimInstance Win32_PageFileUsage | Measure-Object CurrentUsage -Sum).Sum
    $t = Get-Process llama-quantize, llama-imatrix, llama-perplexity, python -ErrorAction SilentlyContinue | Sort-Object WorkingSet64 -Descending | Select-Object -First 1
    "{0},{1:N2},{2:N2},{3},{4},{5:N2},{6:N2}" -f (Get-Date -Format s), ($o.FreePhysicalMemory/1MB), (($o.TotalVirtualMemorySize - $o.FreeVirtualMemory)/1MB), $p, $t.Name, ($t.WorkingSet64/1GB), ($t.PrivateMemorySize64/1GB) | Out-File $f -Append -Encoding utf8
    Start-Sleep 15 } }

# 0a 빌드
if (-not $SkipBuild -or -not (Test-Path "$B\llama-quantize.exe")) {
  "[q1] 0a build $(Stamp)"
  $vc = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat'
  $env:Path = "C:\tools\ninja;C:\Program Files\CMake\bin;$env:Path"
  $cfg = "cmake -G Ninja -S `"$L`" -B `"$L\build`" -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120 -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_SERVER=OFF"
  $bld = "cmake --build `"$L\build`" --target llama-quantize llama-imatrix llama-perplexity llama-gguf-split -j 12"
  cmd /c "`"$vc`" >nul && $cfg > `"$W\build.log`" 2>&1 && $bld >> `"$W\build.log`" 2>&1"
  "[q1] 0a build exit $LASTEXITCODE $(Stamp)"
  Get-Content "$W\build.log" -Tail 3 | ForEach-Object { "[q1]   $_" }
}
foreach ($x in 'llama-quantize', 'llama-imatrix', 'llama-perplexity') { if (-not (Test-Path "$B\$x.exe")) { "[q1] 오류: $x.exe 없음 - 중단"; Stop-Job $memJob; "[q1] done $(Stamp)"; exit 1 } }

# 0b Q8_0
if (-not (Test-Path $q8)) {
  "[q1] 0b q8_0 $(Stamp) mem $(Mem)"
  $t0 = Get-Date
  & "$B\llama-quantize.exe" $bf $q8 Q8_0 $Threads *> "$W\q8_0.log"
  "[q1] 0b q8_0 exit $LASTEXITCODE $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, $([math]::Round((Get-Item $q8 -ErrorAction SilentlyContinue).Length/1GB,2)) GB, mem $(Mem)"
  if ($LASTEXITCODE) { Get-Content "$W\q8_0.log" -Tail 5 | ForEach-Object { "[q1]   $_" }; "[q1] 오류: Q8_0 실패 - 중단"; Stop-Job $memJob; "[q1] done $(Stamp)"; exit 1 }
}
& $py "$R\engine\tools\quant_formats.py" $q8 *> "$W\q8_0-formats.md"
"[q1] 0b q8_0 nextn tensors: $(@(Select-String -Path "$W\q8_0.log" -Pattern 'nextn').Count) lines in log"

# 1 보정 · KL 세트
"[q1] 1 calib $(Stamp)"
& $py "$R\scripts\quant\build_calib.py" --calib "$W\calib.txt" --kl "$W\kl.txt" --manifest "$W\calib-manifest.json" 2>&1 | ForEach-Object { "[q1]   $_" }
if (-not (Test-Path "$W\calib.txt")) { "[q1] 오류: 보정 세트 없음 - 중단"; Stop-Job $memJob; "[q1] done $(Stamp)"; exit 1 }

# 2 imatrix (dense 는 GPU, expert 는 CPU · mmap)
if (-not (Test-Path $imat)) {
  "[q1] 2 imatrix $(Stamp) mem $(Mem)"
  $t0 = Get-Date
  & "$B\llama-imatrix.exe" -m $q8 -f "$W\calib.txt" -o $imat -c 512 --chunks $Chunks -ngl 99 -ot 'ffn_.*_exps=CPU' -t $Threads --parse-special *> "$W\imatrix.log"
  "[q1] 2 imatrix exit $LASTEXITCODE $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, mem $(Mem)"
  Get-Content "$W\imatrix.log" -Tail 4 | ForEach-Object { "[q1]   $_" }
  if ($LASTEXITCODE -or -not (Test-Path $imat)) { "[q1] 오류: imatrix 실패 - 중단"; Stop-Job $memJob; "[q1] done $(Stamp)"; exit 1 }
}

# 3 후보 + G0
foreach ($c in $Cands) {
  $rec = "$R\configs\quant\$c.txt"
  $out = "$R\data\models\qwen36-$c\Qwen3.6-35B-A3B-$($c.ToUpper()).gguf"
  New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
  if (Test-Path $out) { "[q1] 3 $c 이미 있음 - 건너뜀"; continue }
  "[q1] 3 $c start $(Stamp) mem $(Mem)"
  $t0 = Get-Date
  & "$B\llama-quantize.exe" --imatrix $imat --tensor-type-file $rec $bf $out Q8_0 $Threads *> "$W\$c.log"
  $rc = $LASTEXITCODE
  "[q1] 3 $c exit $rc $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min, $([math]::Round((Get-Item $out -ErrorAction SilentlyContinue).Length/1GB,2)) GB, overrides $(@(Select-String -Path "$W\$c.log" -Pattern 'manual override').Count)"
  if ($rc) { Get-Content "$W\$c.log" -Tail 5 | ForEach-Object { "[q1]   $_" }; "[q1] 경고: $c 실패 - 다음 후보로"; continue }
  & $py "$R\engine\tools\quant_formats.py" $out *> "$W\$c-formats.md"
  "[q1] 3 $c G0 $((Get-Content "$W\$c-formats.md" | Select-String 'Routed experts:') -join ' ') sha256 $((Get-FileHash $out -Algorithm SHA256).Hash.ToLower())"
}
Stop-Job $memJob; Remove-Job $memJob -Force
"[q1] mem $(Mem); disk C free $([math]::Round((Get-PSDrive C).Free/1GB)) GB"
"[q1] done $(Stamp)"
