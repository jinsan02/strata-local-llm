# 연속 체인 (11-19 저녁 → 밤): P-diag 1단계 → 64K 점검 → 하네스 추가 후보 A/B → H1 재확인. 한 WMI 프로세스에서 차례로 돈다.
# 각 단계 로그는 단계별 파일(engine\pdiag-chain.log · ctx64-chain.log · hadd-chain.log · h1conf-chain.log), 이 파일은 시작 · 끝만. 끝 표시 '[master] done'.
param([string]$BaseName = 'H0', [string]$BaseArgs = '--harness H0 --tool-out chars --reasoning-echo none --final-turn none')
$ErrorActionPreference = 'Continue'
$b = 'C:\strata-lab\scripts\bench'
$e = 'C:\strata-lab\engine'
"[master] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
"[master] pdiag $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& $b\pdiag-chain.ps1 *>&1 | Out-File -FilePath $e\pdiag-chain.log -Encoding utf8"
"[master] ctx64 $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& $b\ctx64-chain.ps1 *>&1 | Out-File -FilePath $e\ctx64-chain.log -Encoding utf8"
"[master] hadd $(Get-Date -Format s) base $BaseName"
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& $b\hadd-chain.ps1 -BaseName '$BaseName' -BaseArgs '$BaseArgs' *>&1 | Out-File -FilePath $e\hadd-chain.log -Encoding utf8"
"[master] h1conf $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& $b\h1conf-chain.ps1 *>&1 | Out-File -FilePath $e\h1conf-chain.log -Encoding utf8"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[master] done $(Get-Date -Format s)"
