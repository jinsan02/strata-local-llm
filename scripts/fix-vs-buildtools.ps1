# VS Build Tools 재설치 — 1차 설치는 --installPath 의 공백이 쪼개져 C:\Program 에 설치됐다.
$ErrorActionPreference = 'Continue'
$setup = 'C:\Program Files (x86)\Microsoft Visual Studio\Installer\setup.exe'
"[vs-fix] uninstall C:\Program $(Get-Date -Format s)"
$p = Start-Process -FilePath $setup -ArgumentList 'uninstall --installPath "C:\Program" --quiet --norestart --force' -Wait -PassThru
"[vs-fix] uninstall exit $($p.ExitCode); C:\Program exists: $(Test-Path 'C:\Program')"
"[vs-fix] install default path $(Get-Date -Format s)"
$p = Start-Process -FilePath 'C:\strata-lab\downloads\vs_BuildTools.exe' -ArgumentList '--quiet --wait --norestart --nocache --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended' -Wait -PassThru
"[vs-fix] install exit $($p.ExitCode) (0 or 3010 = ok)"
$vw = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
& $vw -all -products * -property installationPath
$vc = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat'
"vcvars64: $(Test-Path $vc)"
if (Test-Path $vc) { cmd /c "`"$vc`" >nul && cl 2>&1" | Select-Object -First 1 }
"[vs-fix] done $(Get-Date -Format s)"
