# 밤 체인 3차를 ssh 작업 객체 밖(WMI)에서 띄운다 (노트북 연결이 끊겨도 산다).
$cmd = 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& C:\strata-lab\scripts\bench\night-chain3.ps1 *>&1 | Out-File -FilePath C:\strata-lab\engine\night-chain3.log -Encoding utf8"'
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $cmd; CurrentDirectory = 'C:\strata-lab'}
"pid $($r.ProcessId) rc $($r.ReturnValue)"
