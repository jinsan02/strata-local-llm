# ssh 작업 객체 밖에서 night-chain 을 띄운다 (Win32_Process.Create 는 WMI 서비스의 자식이라 ssh 종료와 무관).
$cmd = 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& C:\strata-lab\scripts\bench\night-chain.ps1 *>&1 | Out-File -FilePath C:\strata-lab\engine\night-chain.log -Encoding utf8"'
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $cmd; CurrentDirectory = 'C:\strata-lab'}
"pid $($r.ProcessId) rc $($r.ReturnValue)"
