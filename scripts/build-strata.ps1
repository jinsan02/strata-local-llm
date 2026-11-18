# STRATA 고정 커밋 소스 빌드 (E0) — docs/SOURCE_INSTALL.md 의 direct NVIDIA build 경로.
# START-HERE.bat 은 .venv 를 만들고 모델 다운로드까지 할 수 있어 쓰지 않는다.
param(
  [string]$Engine = 'C:\strata-lab\engine',
  [string]$BuildDir = 'build-e0',
  [string]$Arch = '120',
  [int]$Jobs = 12          # nvcc 병렬은 RAM 을 많이 쓴다. 32GB 에서 12 로 시작
)
$ErrorActionPreference = 'Continue'
$vc = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat'
$cmake = 'C:\Program Files\CMake\bin\cmake.exe'
$env:Path = "C:\tools\ninja;C:\Program Files\CMake\bin;$env:Path"
Set-Location $Engine
$commit = (git rev-parse HEAD).Trim()
$tag = (git describe --tags --always).Trim()
$dirty = if (git status --porcelain) { 1 } else { 0 }
"[build] engine $tag $commit dirty=$dirty  $(Get-Date -Format s)"
$log = Join-Path $Engine "$BuildDir.log"
$cfg = "`"$cmake`" -G Ninja -S . -B $BuildDir -DCMAKE_BUILD_TYPE=Release -DSTRATA_ENABLE_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=$Arch"
$bld = "`"$cmake`" --build $BuildDir --target strata -j $Jobs"
"[build] configure: $cfg"
"[build] build: $bld"
$t0 = Get-Date
cmd /c "`"$vc`" >nul && $cfg > `"$log`" 2>&1 && $bld >> `"$log`" 2>&1"
$rc = $LASTEXITCODE
$min = [math]::Round(((Get-Date) - $t0).TotalMinutes, 1)
"[build] exit $rc  ($min min)  full log: $log"
Get-Content $log -Tail 15
$exe = Get-ChildItem $BuildDir -Recurse -Filter 'strata*.exe' -ErrorAction SilentlyContinue | Select-Object -First 5
foreach ($e in $exe) { "[build] output $($e.FullName)  $([math]::Round($e.Length/1MB,1)) MB  sha256 $((Get-FileHash $e.FullName -Algorithm SHA256).Hash.ToLower())" }
"[build] done $(Get-Date -Format s)"
