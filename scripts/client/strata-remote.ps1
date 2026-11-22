# 노트북에서 Tailscale 로 본체 STRATA 서버를 부른다 (OpenAI 호환 API).
# 연결 확인용이다. 성능 측정 기록은 본체에서 같은 조건으로 재는 측정 러너가 원장에 쓴다
# (이 결과에는 Tailscale 왕복 지연이 섞인다).
#
# 준비 (노트북, 한 번):
#   API 키는 파일에 쓰지 않는다. 사용자 환경 변수로 둔다.
#   [Environment]::SetEnvironmentVariable('STRATA_API_KEY', '<키>', 'User')   # 새 터미널부터 적용
#
# 예:
#   .\strata-remote.ps1                       # 모델 목록 + 짧은 질문 하나
#   .\strata-remote.ps1 -Prompt "파이썬으로 피보나치 함수를 써 줘" -MaxTokens 256
#   .\strata-remote.ps1 -ModelsOnly
param(
  [string]$BaseUrl = $(if ($env:STRATA_BASE_URL) { $env:STRATA_BASE_URL } else { throw 'STRATA_BASE_URL 을 설정하세요 (예: http://<본체 Tailscale 주소>:8080)' }),
  [string]$Prompt = '한 문장으로 자기소개를 해 줘.',
  [int]$MaxTokens = 128,
  [switch]$ModelsOnly
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$headers = @{}
if ($env:STRATA_API_KEY) { $headers['Authorization'] = "Bearer $($env:STRATA_API_KEY)" }
else { Write-Warning 'STRATA_API_KEY 가 없다. 서버가 키를 요구하면 401 이 난다.' }

$hostPart = ([Uri]$BaseUrl).Host; $port = ([Uri]$BaseUrl).Port
Write-Host "== 연결 $BaseUrl"
$tcp = Test-NetConnection $hostPart -Port $port -WarningAction SilentlyContinue
if (-not $tcp.TcpTestSucceeded) {
  Write-Host "   TCP $port 연결 실패. 확인: 본체 서버가 --access tailscale 로 떠 있는가, 본체 방화벽 규칙(docs/ENVIRONMENT.md), tailscale status" -ForegroundColor Red
  exit 2
}
Write-Host "   TCP $port 열림 (ping $($tcp.PingReplyDetails.RoundtripTime) ms)"

Write-Host '== 모델 목록 (/v1/models)'
$models = Invoke-RestMethod -Uri "$BaseUrl/v1/models" -Headers $headers -TimeoutSec 30
$ids = @($models.data | ForEach-Object { $_.id })
$ids | ForEach-Object { Write-Host "   $_" }
if ($ModelsOnly -or -not $ids) { exit 0 }

Write-Host "== 질문 (/v1/chat/completions, max_tokens $MaxTokens, stream 끔)"
$body = @{ model = $ids[0]; max_tokens = $MaxTokens; stream = $false
           messages = @(@{ role = 'user'; content = $Prompt }) } | ConvertTo-Json -Depth 5
$sw = [Diagnostics.Stopwatch]::StartNew()
$r = Invoke-RestMethod -Uri "$BaseUrl/v1/chat/completions" -Method Post -Headers $headers `
       -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 600
$sw.Stop()
$msg = $r.choices[0].message
if ($msg.reasoning_content) { Write-Host "   [reasoning] $($msg.reasoning_content)" -ForegroundColor DarkGray }
Write-Host "   $($msg.content)"
$u = $r.usage
Write-Host ("== 완료 {0:N1}s · prompt {1} · completion {2} 토큰 · 종료 사유 {3}  (Tailscale 왕복 포함, 측정 기록용 아님)" -f `
  $sw.Elapsed.TotalSeconds, $u.prompt_tokens, $u.completion_tokens, $r.choices[0].finish_reason)
