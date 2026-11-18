# 밤 체인 2차를 ssh 작업 객체 밖(WMI)에서 띄운다. 1차가 끝날 때까지 스스로 기다린다.
$cmd = 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& C:\Users\jinsan\AppData\Local\Temp\x3\v4\night-chain2.ps1 *>&1 | Out-File -FilePath C:\strata-lab\engine\night-chain2.log -Encoding utf8"'
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $cmd; CurrentDirectory = 'C:\strata-lab'}
"pid $($r.ProcessId) rc $($r.ReturnValue)"
