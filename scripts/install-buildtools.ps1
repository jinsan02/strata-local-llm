# VS 2022 Build Tools(C++), CUDA 13.2.2(드라이버 제외), CMake 4.1.2, Ninja 1.13.1 설치
$ErrorActionPreference = 'Continue'
$dl = 'C:\strata-lab\downloads'; New-Item -ItemType Directory -Force $dl | Out-Null
function Get-File($url, $name) { $f = Join-Path $dl $name; if (-not (Test-Path $f)) { curl.exe -sSL --retry 3 -o $f $url }; "$name sha256 $((Get-FileHash $f -Algorithm SHA256).Hash.ToLower())"; return }

# 1) VS 2022 Build Tools
Get-File 'https://aka.ms/vs/17/release/vs_BuildTools.exe' 'vs_BuildTools.exe'
"[vs] installing $(Get-Date -Format s)"
# --installPath 를 배열 인자로 넘기면 공백에서 쪼개져 C:\Program 에 설치된다(2026-11-18).
# 기본 경로(...\2022\BuildTools)를 쓰고, 인자는 한 문자열로 넘긴다.
$p = Start-Process "$dl\vs_BuildTools.exe" -ArgumentList '--quiet --wait --norestart --nocache --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended' -Wait -PassThru
"[vs] exit $($p.ExitCode) (0 or 3010 = ok)"

# 2) CUDA 13.2.2 toolkit only
Get-File 'https://developer.download.nvidia.com/compute/cuda/13.2.2/network_installers/cuda_13.2.2_windows_network.exe' 'cuda_13.2.2_windows_network.exe'
$pk = 'crt cublas cublas_dev cuda_profiler_api cudart cufft cufft_dev cuobjdump cupti curand curand_dev cusolver cusolver_dev cusparse cusparse_dev cuxxfilt nsight_compute nsight_systems npp npp_dev nvcc nvdisasm nvfatbin nvjitlink nvml_dev nvprune nvptxcompiler nvrtc nvrtc_dev nvtx nvvm sanitizer thrust visual_studio_integration'.Split(' ') | ForEach-Object { "${_}_13.2" }
"[cuda] installing $(Get-Date -Format s)"
$p = Start-Process "$dl\cuda_13.2.2_windows_network.exe" -ArgumentList (@('-s') + $pk + @('-n')) -Wait -PassThru
"[cuda] exit $($p.ExitCode)"

# 3) CMake
Get-File 'https://github.com/Kitware/CMake/releases/download/v4.1.2/cmake-4.1.2-windows-x86_64.msi' 'cmake-4.1.2-windows-x86_64.msi'
$p = Start-Process msiexec.exe -ArgumentList '/i',"$dl\cmake-4.1.2-windows-x86_64.msi",'/qn','/norestart','ADD_CMAKE_TO_PATH=System' -Wait -PassThru
"[cmake] exit $($p.ExitCode)"

# 4) Ninja -> C:\tools\ninja (system PATH)
Get-File 'https://github.com/ninja-build/ninja/releases/download/v1.13.1/ninja-win.zip' 'ninja-win.zip'
New-Item -ItemType Directory -Force C:\tools\ninja | Out-Null
Expand-Archive -Force "$dl\ninja-win.zip" C:\tools\ninja
$mp = [Environment]::GetEnvironmentVariable('Path','Machine')
if ($mp -notlike '*C:\tools\ninja*') { [Environment]::SetEnvironmentVariable('Path', "$mp;C:\tools\ninja", 'Machine') }
"[ninja] $(& C:\tools\ninja\ninja.exe --version)"

# verify
"== verify $(Get-Date -Format s)"
$vc = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat'
"vcvars64: $(Test-Path $vc)"
cmd /c "`"$vc`" >nul && cl 2>&1 | findstr Version"
$nvcc = Get-ChildItem 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\*\bin\nvcc.exe' -ErrorAction SilentlyContinue | Select -First 1
if ($nvcc) { & $nvcc.FullName --version | Select-String release } else { "nvcc not found" }
& 'C:\Program Files\CMake\bin\cmake.exe' --version | Select -First 1
nvidia-smi --query-gpu=driver_version --format=csv,noheader
"== done"
