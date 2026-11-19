# 연속 체인(P-diag 1 → 64K → 하네스 추가 A/B → H1 재확인)을 ssh 작업 객체 밖(WMI)에서 띄운다 (노트북 연결이 끊겨도 산다).
#   powershell -ExecutionPolicy Bypass -File launch_master.ps1 [-BaseName H0] [-BaseArgs '--harness H0 --tool-out chars --reasoning-echo none --final-turn none']
param([string]$BaseName = 'H0', [string]$BaseArgs = '--harness H0 --tool-out chars --reasoning-echo none --final-turn none')
$inner = "& C:\strata-lab\scripts\bench\master-chain.ps1 -BaseName '$BaseName' -BaseArgs '$BaseArgs' *>&1 | Out-File -FilePath C:\strata-lab\engine\master-chain.log -Encoding utf8"
$cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command `"$inner`""
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $cmd; CurrentDirectory = 'C:\strata-lab'}
"pid $($r.ProcessId) rc $($r.ReturnValue) base $BaseName"
