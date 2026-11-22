# 노트북에서 Claude Code 를 본체 STRATA(로컬 LLM)에 붙여 실행한다.
# 환경 변수는 이 프로세스에만 건다. ~/.claude/settings.json 을 고치지 않으므로
# 평소 Claude Code(Anthropic 계정)는 그대로다.
# 값은 `strata connect claude-code` (v0.2.15) 안내를 따른다. 주소만 Tailscale 로 바꿨다.
#
# 예:  .\claude-local.ps1                 # 대화형
#      .\claude-local.ps1 -p "이 폴더의 README 를 요약해 줘"
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$ClaudeArgs)
$base = if ($env:STRATA_BASE_URL) { $env:STRATA_BASE_URL } else { throw 'STRATA_BASE_URL 을 설정하세요 (예: http://<본체 Tailscale 주소>:8080)' }
$ctx  = if ($env:STRATA_CONTEXT) { $env:STRATA_CONTEXT } else { '32768' }   # 서버의 --context 와 같게
$env:ANTHROPIC_BASE_URL = $base             # /v1 을 붙이지 않는다 (Claude Code 가 /v1/messages 를 붙인다)
$env:ANTHROPIC_AUTH_TOKEN = $(if ($env:STRATA_API_KEY) { $env:STRATA_API_KEY } else { 'strata-local' })
foreach ($k in 'ANTHROPIC_MODEL','ANTHROPIC_SMALL_FAST_MODEL','ANTHROPIC_DEFAULT_SONNET_MODEL','ANTHROPIC_DEFAULT_OPUS_MODEL','ANTHROPIC_DEFAULT_HAIKU_MODEL') {
  Set-Item "env:$k" 'strata'
}
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = '1'
$env:DISABLE_AUTOUPDATER = '1'
$env:DISABLE_TELEMETRY = '1'
# 예산 (docs/plan-v2.1-amendment-20261118.md 4절): 출력+reasoning = 창의 1/4 (32K → 8,192), 입력 = 나머지 3/4 (24,576).
# STRATA 권장 4096 보다 크게 잡았다. reasoning 이 예산을 자주 다 쓰면 다시 조정하고 이유를 기록한다.
$out = [int]([int]$ctx / 4)
$env:CLAUDE_CODE_MAX_CONTEXT_TOKENS = $ctx
$env:CLAUDE_CODE_MAX_OUTPUT_TOKENS = "$out"
$env:CLAUDE_CODE_SIMPLE = '1'               # 전체 프롬프트 15.6K 토큰 → 1.25K (32K 창에서 권장)
Write-Host "Claude Code → STRATA $base (context $ctx, 입력 $([int]$ctx - $out), 출력+reasoning $out)" -ForegroundColor Cyan
# 데스크톱 앱과 ~/.claude 를 같이 쓰므로 거기 등록된 MCP(strata-worker 등)가 붙어 프롬프트가 커진다. 측정 · 로컬 실행에서는 뺀다.
& claude --strict-mcp-config @ClaudeArgs
