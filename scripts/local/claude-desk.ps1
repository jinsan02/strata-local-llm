# 본체에서 Claude Code CLI(2.1.328, 노트북과 같은 파일)를 STRATA 에 붙여 실행한다. Tailscale 왕복 없음.
# 환경 변수는 이 프로세스에만 건다. -TestEnv 를 주면 그 conda 환경의 python 이 PATH 맨 앞에 오고
# PYTHONPATH=<현재 폴더>\src 가 걸려, 모델의 Bash 도구에서 `python -m pytest -q tests/...` 가 바로 돈다.
#
#   cd <저장소>; C:\strata-lab\scripts\local\claude-desk.ps1 -TestEnv packaging          # 대화형
#   C:\strata-lab\scripts\local\claude-desk.ps1 -TestEnv flask -p "..."                 # 한 번 실행
#   ... -InFile <지시문 파일>   # 지시문을 stdin 으로 (x4d-task)
# param 블록을 쓰지 않는다(11-24): [Parameter] 가 있으면 -p 가 -PipelineVariable 에, 없으면 남는 인자가 위치로 -InFile 에 묶였다.
# -TestEnv · -InFile 두 쌍만 직접 떼어 내고 나머지는 claude 에 그대로 넘긴다.
$TestEnv = 'none'; $InFile = ''; $ClaudeArgs = @()
for ($i = 0; $i -lt $args.Count; $i++) {
  if ($args[$i] -ceq '-TestEnv') { $TestEnv = $args[++$i] }
  elseif ($args[$i] -ceq '-InFile') { $InFile = $args[++$i] }
  else { $ClaudeArgs += , $args[$i] }
}
if ($TestEnv -notin @('none', 'packaging', 'flask')) { throw "-TestEnv 는 none · packaging · flask (받은 값: $TestEnv)" }
$Exe = Join-Path $env:USERPROFILE '.local\bin\claude-2.1.328\claude.exe'
if (-not (Test-Path $Exe)) { throw "Claude Code 실행 파일 없음: $Exe" }
# 서버 주소: STRATA_BASE_URL > 8080 을 듣는 주소(127.0.0.1 이든 Tailscale 이든)
$base = $env:STRATA_BASE_URL
if (-not $base) {
  $a = @(Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { $_.LocalAddress }) | Select-Object -First 1
  if (-not $a) { throw '8080 을 듣는 서버가 없다. 먼저 strata-up.ps1' }
  if ($a -in @('0.0.0.0', '::')) { $a = '127.0.0.1' }
  $base = "http://${a}:8080"
}
$ctx = if ($env:STRATA_CONTEXT) { $env:STRATA_CONTEXT } else { '65536' }   # 서버 --context 와 같게
$out = [math]::Min([int]([int]$ctx / 4), 8192)
$env:ANTHROPIC_BASE_URL = $base
$env:ANTHROPIC_AUTH_TOKEN = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()   # 값은 출력하지 않는다
foreach ($k in 'ANTHROPIC_MODEL', 'ANTHROPIC_SMALL_FAST_MODEL', 'ANTHROPIC_DEFAULT_SONNET_MODEL', 'ANTHROPIC_DEFAULT_OPUS_MODEL', 'ANTHROPIC_DEFAULT_HAIKU_MODEL') { Set-Item "env:$k" 'strata' }
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = '1'
$env:DISABLE_AUTOUPDATER = '1'
$env:DISABLE_TELEMETRY = '1'
$env:CLAUDE_CODE_MAX_CONTEXT_TOKENS = $ctx
$env:CLAUDE_CODE_MAX_OUTPUT_TOKENS = "$out"
$env:CLAUDE_CODE_SIMPLE = '1'
if ($TestEnv -ne 'none') {
  $py = @{ packaging = 'C:\ProgramData\anaconda3\envs\x3_packaging'; flask = 'C:\ProgramData\anaconda3\envs\swe_flask_5014' }[$TestEnv]
  $env:PATH = "$py;$py\Scripts;$env:PATH"
  $env:PYTHONPATH = Join-Path (Get-Location) 'src'
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTHONUTF8 = '1'
  # 11-24: 모델 셸에서 인터넷을 막는다(urllib · requests · pip · git 은 프록시 변수를 따른다). 서버(127.0.0.1)는 NO_PROXY 로 뺀다.
  # 원시 소켓까지 막지는 못하므로 x4d-task 의 기록 검사(audit)와 같이 쓴다.
  foreach ($k in 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy') { Set-Item "env:$k" 'http://127.0.0.1:9' }
  $env:NO_PROXY = '127.0.0.1,localhost'; $env:no_proxy = '127.0.0.1,localhost'
  $env:PIP_NO_INDEX = '1'
}
Write-Host "Claude Code(본체) → $base (context $ctx, 출력+reasoning $out, 테스트 환경 $TestEnv)" -ForegroundColor Cyan
if ($InFile) {
  $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
  Get-Content -Raw -Encoding utf8 $InFile | & $Exe --strict-mcp-config @ClaudeArgs
} else {
  & $Exe --strict-mcp-config @ClaudeArgs
}
