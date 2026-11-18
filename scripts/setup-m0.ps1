# STRATA 소스 setup 으로 M0 실행 구성을 만든다 (서버는 띄우지 않는다).
# setup.py 는 자기를 실행한 Python 에 패키지를 깐다 → conda 환경 strata_local_llm 으로 부른다(.venv 없음).
# --build: 고정 커밋에서 엔진을 engine\build 에 빌드. --gguf-dir: 받아 둔 M0 를 그대로 쓴다.
param(
  [int]$Context = 8192,
  [string]$Gguf = 'C:\strata-lab\data\models\qwen36-ud-q4_k_xl'
)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:STRATA_VCVARS = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat'
$env:Path = "C:\tools\ninja;C:\Program Files\CMake\bin;$env:Path"
$env:PYTHONUTF8 = '1'
Set-Location C:\strata-lab\engine
"[setup] engine $(git rev-parse HEAD) dirty=$(if (git status --porcelain) {1} else {0})  context=$Context  $(Get-Date -Format s)"
$t0 = Get-Date
& $py setup.py --family qwen36 --model UD-Q4_K_XL --gguf-dir $Gguf --data-dir C:\strata-lab\data `
  --context $Context --parallel 1 --vision no --build --no-start --no-browser --yes 2>&1
"[setup] exit $LASTEXITCODE  $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min"
Get-ChildItem C:\strata-lab\engine -Filter 'strata-*.json' | Select Name,Length,LastWriteTime | Out-String
Get-ChildItem C:\strata-lab\engine -Filter 'run-*.bat' | Select Name,LastWriteTime | Out-String
if (Test-Path C:\strata-lab\engine\build\strata.exe) { "[setup] build\strata.exe sha256 $((Get-FileHash C:\strata-lab\engine\build\strata.exe).Hash.ToLower())" }
"[setup] done $(Get-Date -Format s)"
