# 본체 안에서 쓸 STRATA 서버를 띄운다(기본 127.0.0.1 전용, 64K · E2). 떠 있는 서버는 내리고 다시 띄운다.
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\local\strata-up.ps1              # 본체 전용
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\local\strata-up.ps1 -Tailscale   # 노트북에서도 (키 필수)
#   ... -LlmMode   # 측정급: 백그라운드 정리 · 전원 고정 뒤 띄움
param([int]$Context = 65536, [switch]$Tailscale, [switch]$LlmMode)
$p = @{ Context = $Context }
if (-not $Tailscale) { $p.Host_ = '127.0.0.1' }
if ($LlmMode) { $p.LlmMode = $true }
# 떠 있는 서버를 먼저 내린다: 그 서버가 serve-detached.log 를 잡고 있으면 새 서버의 Out-File 이 열지 못해 바로 죽는다(11-24 확인)
& C:\strata-lab\scripts\serve-ctx.ps1 -Stop
& C:\strata-lab\scripts\launch_serve.ps1 @p
exit $LASTEXITCODE
