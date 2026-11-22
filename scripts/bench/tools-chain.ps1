# 11-22 도구 측정 초안 (docs/tools-20261122.md 7절). 노력치 체인 결과로 -Effort 와 대조를 정한 뒤 돌린다.
# 팔 T1: H7 + card-coding + 노력치 + 편집 직후 문법 검사. 팔 T2: T1 + outline · read_symbol. 둘 다 64K 서버, 6과제 x 5회.
param([ValidateSet('low', 'medium', 'high', 'xhigh')][string]$Effort = 'medium')
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'
$tag = @{ low = 'l'; medium = 'm'; high = 'h'; xhigh = 'x' }[$Effort]
"[tools] start $(Get-Date -Format s) commit $(git -C $R rev-parse --short HEAD) effort $Effort"
"[tools] arm T1 syntax-check $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\bench\g3-chain.ps1" -Only M0 -ForceX3 -Harness H7T1 -Prefix "x3t1$tag" -EditApply lenient -Reps 5 -Context 65536 -Effort $Effort -SyntaxCheck
"[tools] arm T2 syntax-check + code-tools $(Get-Date -Format s)"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\bench\g3-chain.ps1" -Only M0 -ForceX3 -Harness H7T2 -Prefix "x3t2$tag" -EditApply lenient -Reps 5 -Context 65536 -Effort $Effort -SyntaxCheck -CodeTools
"[tools] done $(Get-Date -Format s)"
