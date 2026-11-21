# 11-22 노력치 측정 (docs/effort-20261122.md, STATE 26). 서버는 둘 다 64K. M0 · H7(--edit-apply lenient) · card-coding · 6과제 x 5회.
# 팔 M: medium(문턱 22,272 · 호출 20) = 64K 서버에서 기존 32K 설정과 같은지. 대조 x3h7 17/30.
# 팔 X: xhigh(문턱 55,296 · 호출 30). 대조 x3k64h7(high) 21/30.
# 각 g3-chain 이 서버 기동 · 측정 · 종료 · 모드 전환을 한다. 끝 표시 '[effort] done'.
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'
"[effort] start $(Get-Date -Format s) commit $(git -C $R rev-parse --short HEAD)"
"[effort] arm M medium 64K $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\bench\g3-chain.ps1" -Only M0 -ForceX3 -Harness H7 -Prefix x3e64m -EditApply lenient -Reps 5 -Context 65536 -Effort medium
"[effort] arm X xhigh 64K $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\bench\g3-chain.ps1" -Only M0 -ForceX3 -Harness H7 -Prefix x3exh -EditApply lenient -Reps 5 -Context 65536 -Effort xhigh
"[effort] done $(Get-Date -Format s)"
