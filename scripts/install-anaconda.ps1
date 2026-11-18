$ErrorActionPreference = 'Stop'
$dl = 'C:\strata-lab\downloads'; New-Item -ItemType Directory -Force $dl | Out-Null
$f = Join-Path $dl 'Anaconda3-2026.07-1-Windows-x86_64.exe'
$want = 'b545f4bd8ab3bf32d99002a0779a887668ebfe479ee32ecbf060375670d5ee09'
if (-not (Test-Path $f) -or (Get-FileHash $f -Algorithm SHA256).Hash.ToLower() -ne $want) {
  curl.exe -sSL --retry 3 -o $f https://repo.anaconda.com/archive/Anaconda3-2026.07-1-Windows-x86_64.exe
}
$got = (Get-FileHash $f -Algorithm SHA256).Hash.ToLower()
"sha256 $got"
if ($got -ne $want) { throw "hash mismatch" }
"installing..."
$p = Start-Process -FilePath $f -ArgumentList '/InstallationType=AllUsers','/RegisterPython=0','/AddToPath=0','/S','/D=C:\ProgramData\anaconda3' -Wait -PassThru
"installer exit $($p.ExitCode)"
$conda = 'C:\ProgramData\anaconda3\Scripts\conda.exe'
& $conda --version
& $conda create -y -n strata_local_llm --override-channels -c conda-forge python=3.12 2>&1 | Select-Object -Last 5
& $conda env list
& 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe' --version
Test-Path 'C:\ProgramData\anaconda3\Scripts\anaconda-navigator.exe'
