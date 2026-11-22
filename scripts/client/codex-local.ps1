# 노트북에서 Codex CLI 를 본체 STRATA(로컬 LLM)에 붙여 실행한다.
# 평소 ~/.codex/config.toml 을 건드리지 않도록 별도 CODEX_HOME(~/.codex-strata)을 쓴다.
# 값은 `strata connect codex` (v0.2.15) 안내를 따른다. 주소만 Tailscale 로 바꿨다.
#
# 예:  .\codex-local.ps1
#      .\codex-local.ps1 exec --skip-git-repo-check "이 함수에 테스트를 써 줘"
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$CodexArgs)
$base = if ($env:STRATA_BASE_URL) { $env:STRATA_BASE_URL } else { throw 'STRATA_BASE_URL 을 설정하세요 (예: http://<본체 Tailscale 주소>:8080)' }
$ctx  = if ($env:STRATA_CONTEXT) { $env:STRATA_CONTEXT } else { '32768' }   # 서버의 --context 와 같게
$home2 = Join-Path $env:USERPROFILE '.codex-strata'
New-Item -ItemType Directory -Force $home2 | Out-Null
# 예산 (docs/plan-v2.1-amendment-20261118.md 4절): 출력+reasoning = 창의 1/4 (32K → 8,192),
# 입력 예산 3/4 (24,576) 에 닿기 전에 요약: 약 61% (32K → 20,000).
$out = [int]([int]$ctx / 4)
$compact = [int]([math]::Round([int]$ctx * 0.61 / 1000) * 1000)
$cfg = @"
model = "strata"
model_provider = "strata"
model_context_window = $ctx
model_max_output_tokens = $out
model_auto_compact_token_limit = $compact
model_reasoning_summary = "auto"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
check_for_update_on_startup = false

[model_providers.strata]
name = "Strata (desktop-5070)"
base_url = "$base/v1"
wire_api = "responses"
env_key = "STRATA_API_KEY"
stream_idle_timeout_ms = 600000
"@
[IO.File]::WriteAllText((Join-Path $home2 'config.toml'), $cfg, (New-Object Text.UTF8Encoding($false)))
$env:CODEX_HOME = $home2
if (-not $env:STRATA_API_KEY) { $env:STRATA_API_KEY = 'strata-local' }
Write-Host "Codex → STRATA $base/v1 (context $ctx, 출력+reasoning $out, 요약 기준 $compact, CODEX_HOME $home2)" -ForegroundColor Cyan
& codex @CodexArgs
