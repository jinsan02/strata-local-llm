# 노트북에서 Claude Code 를 본체 STRATA(로컬 LLM)에 붙여 실행한다.
# 환경 변수는 이 프로세스에만 건다. ~/.claude/settings.json 을 고치지 않으므로
# 평소 Claude Code(Anthropic 계정)는 그대로다.
# 값은 `strata connect claude-code` (v0.2.15) 안내를 따른다. 주소만 Tailscale 로 바꿨다.
#
# 예:  .\claude-local.ps1                 # 대화형
#      .\claude-local.ps1 -p "이 폴더의 README 를 요약해 줘"
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$ClaudeArgs)
$base = if ($env:STRATA_BASE_URL) { $env:STRATA_BASE_URL } else { 'http://100.121.174.83:8080' }
$ctx  = if ($env:STRATA_CONTEXT) { $env:STRATA_CONTEXT } else { '32768' }   # 서버의 --context 와 같게
$env:ANTHROPIC_BASE_URL = $base             # /v1 을 붙이지 않는다 (Claude Code 가 /v1/messages 를 붙인다)
$env:ANTHROPIC_AUTH_TOKEN = $(if ($env:STRATA_API_KEY) { $env:STRATA_API_KEY } else { 'strata-local' })
foreach ($k in 'ANTHROPIC_MODEL','ANTHROPIC_SMALL_FAST_MODEL','ANTHROPIC_DEFAULT_SONNET_MODEL','ANTHROPIC_DEFAULT_OPUS_MODEL','ANTHROPIC_DEFAULT_HAIKU_MODEL') {
  Set-Item "env:$k" 'strata'
}
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = '1'
$env:DISABLE_AUTOUPDATER = '1'
$env:DISABLE_TELEMETRY = '1'
$env:CLAUDE_CODE_MAX_CONTEXT_TOKENS = $ctx
$env:CLAUDE_CODE_MAX_OUTPUT_TOKENS = '4096'
$env:CLAUDE_CODE_SIMPLE = '1'               # 전체 프롬프트 15.6K 토큰 → 1.25K (32K 창에서 권장)
Write-Host "Claude Code → STRATA $base (context $ctx)" -ForegroundColor Cyan
& claude @ClaudeArgs
