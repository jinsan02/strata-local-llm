# 11-21 25-4 (docs/l2-mask-20261121.md): A = 32K + L2 마스킹(x3l2) → B = 64K 마스킹 없음(x3k64h7). 둘 다 M0 · H7(--edit-apply lenient) · card-coding · 6과제 x 5회.
# 대조 = x3h7 17/30 (다시 안 돌림). 각 g3-chain 이 서버 기동 · 측정 · 종료 · 모드 전환을 한다. 끝 표시 '[l2] done'.
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'
"[l2] start $(Get-Date -Format s) commit $(git -C $R rev-parse --short HEAD)"
"[l2] arm A 32K mask $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\bench\g3-chain.ps1" -Only M0 -ForceX3 -Harness H7L2 -Prefix x3l2 -EditApply lenient -Reps 5 -Context 32768 -Mask
"[l2] arm B 64K $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\bench\g3-chain.ps1" -Only M0 -ForceX3 -Harness H7 -Prefix x3k64h7 -EditApply lenient -Reps 5 -Context 65536
"[l2] done $(Get-Date -Format s)"
