# X4b (본체): Claude Code CLI 로 X3 · Y 과제 하나를 본체 안에서 풀고(테스트 실행 허용) 같은 채점기로 채점한다.
# 노트북 X4(x4-task.ps1)와 다른 점: Tailscale 왕복 없음, 모델이 Bash 로 pytest 를 돌릴 수 있음.
# 작업 폴더는 C:\strata-x4d\<run> (C:\strata-lab 밖). 숨은 테스트 · 참조 패치는 작업 폴더에 넣지 않고,
# 끝난 뒤 클라이언트 기록에서 저장소 밖 경로(strata-lab · private · ref.patch · hidden) 접근을 검사해 meta.audit 에 적는다.
#
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\local\x4d-task.ps1 -Set y -Task y2_wheel_build_number -Rep 1
param([ValidateSet('x3', 'y')][string]$Set = 'y', [Parameter(Mandatory = $true)][string]$Task, [int]$Rep = 1,
      [int]$MaxTurns = 40, [string]$Prefix = 'x4d', [switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Lab = 'C:\strata-lab'
$Root = 'C:\strata-x4d'
$Priv = Join-Path $Root '_private'
$RunName = "${Prefix}_${Task}_r$Rep"
$Work = Join-Path $Root $RunName
$SetDir = if ($Set -eq 'y') { 'y-set' } else { 'x3-packaging' }
$TaskDir = "$Lab\configs\eval\$SetDir\$Task"
New-Item -ItemType Directory -Force $Priv | Out-Null
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$Cfg = Get-Content "$TaskDir\task.json" -Raw -Encoding utf8 | ConvertFrom-Json
$RepoName = if ($Cfg.repo) { $Cfg.repo } else { 'packaging' }
$Commit = @{ packaging = '6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc'; flask = '7ee9ceb71e868944a46e1ff00b506772a53a4f1d' }[$RepoName]
$Label = @{ packaging = 'pypa/packaging'; flask = 'pallets/flask' }[$RepoName]

# 1) 작업 복사본: X4 와 같은 git bundle · 고정 커밋, setup_patch 는 커밋으로
if (Test-Path $Work) { Remove-Item -Recurse -Force $Work }
git clone -q --no-checkout "$Lab\work\x4\bundles\$RepoName.bundle" $Work
git -C $Work -c core.autocrlf=false checkout -q --detach $Commit
if ($Cfg.setup_patch) { git -C $Work apply "$TaskDir\$($Cfg.setup_patch)" }
git -C $Work -c core.autocrlf=false add -A
git -C $Work -c user.name=x4 -c user.email=x4@localhost commit -q --allow-empty -m setup

# 2) 지시문: 과제 원문 + 환경 안내 (테스트 실행 가능)
$Allow = @($Cfg.write_allow)
$Rule = if ($Allow.Count -and $Allow[0]) { "테스트 파일은 고치지 마라. 새로 만들 파일: $($Allow -join ', ')" } else { '테스트 파일은 고치지 마라.' }
$Note = "너는 $Label 저장소(현재 폴더, 고정 커밋)에서 작업한다. 코드는 Edit · Write 도구로 고치고, Bash 도구로 ``python -m pytest -q tests/<파일>`` 을 돌려 확인할 수 있다(PYTHONPATH=src 는 이미 설정됨). 셸 명령은 이 형태와 ``python -c`` · ``git diff`` · ``git status`` 만 허용되고, 파이프(|) · 2>&1 · 환경 변수 접두사를 붙이면 막힌다. 저장소 밖 파일은 보지 마라. $Rule"
$PromptFile = "$Priv\$RunName.prompt.txt"
[IO.File]::WriteAllText($PromptFile, (Get-Content "$TaskDir\prompt.md" -Raw -Encoding utf8) + "`r`n`r`n" + $Note, $Utf8)

# 3) 클라이언트: 개인 설정 · MCP 없이. Bash 는 pytest · python -c · git diff/status 만
$ClientArgs = @('-p', '--output-format', 'stream-json', '--verbose', '--max-turns', "$MaxTurns", '--bare', '--setting-sources', 'project', '--no-session-persistence',
                '--permission-mode', 'acceptEdits',
                '--allowedTools', 'Read,Edit,Write,Glob,Grep,Bash(python -m pytest:*),Bash(python -c:*),Bash(git diff:*),Bash(git status:*)',
                '--disallowedTools', 'WebFetch,WebSearch,Task')
$env:STRATA_CONTEXT = '65536'
$TestEnv = $RepoName
$T0 = Get-Date
$Ram0 = [int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1024)
if ($DryRun) {
  "[x4d] DryRun: $Work 준비 끝. claude-desk.ps1 -TestEnv $TestEnv -PromptFile $PromptFile $($ClientArgs -join ' ')"
  $Raw = '{"dry_run": true}'
  $RamMin = $Ram0
} else {
  # RAM 여유를 5초마다 잰다(서버 + 클라이언트 동시)
  $Mon = Start-Job { $m = 999999; while ($true) { $f = [int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1024); if ($f -lt $m) { $m = $f; Set-Content "$using:Priv\$using:RunName.rammin" $m }; Start-Sleep 5 } }
  Push-Location $Work
  [Console]::OutputEncoding = $Utf8
  $ErrorActionPreference = 'Continue'   # claude 의 stderr 경고(unrecognized_model)가 멈추게 하지 않게
  try { $Raw = (& "$Lab\scripts\local\claude-desk.ps1" -TestEnv $TestEnv -PromptFile $PromptFile @ClientArgs) -join "`n" }
  finally { Pop-Location; $ErrorActionPreference = 'Stop'; Stop-Job $Mon; Remove-Job $Mon -Force }
  $RamMin = if (Test-Path "$Priv\$RunName.rammin") { [int](Get-Content "$Priv\$RunName.rammin") } else { $null }
}
$Wall = [math]::Round(((Get-Date) - $T0).TotalSeconds, 1)
[IO.File]::WriteAllText("$Priv\$RunName.client.jsonl", "$Raw", $Utf8)
$Meta = [ordered]@{ wall_s = $Wall; client = 'claude-code-desk'; client_version = '2.1.328'; max_turns = $MaxTurns; dry_run = [bool]$DryRun;
                    ram_free_start_mb = $Ram0; ram_free_min_mb = $RamMin }
try {
  $Last = ($Raw -split "`n" | Where-Object { $_ -match '"type":"result"' } | Select-Object -Last 1)
  $J = $Last | ConvertFrom-Json
  $Meta.num_turns = $J.num_turns; $Meta.is_error = $J.is_error; $Meta.duration_ms = $J.duration_ms; $Meta.usage = $J.usage
  $Meta.result_head = "$($J.result)".Substring(0, [math]::Min(400, "$($J.result)".Length))
  $Names = [regex]::Matches($Raw, '"type":"tool_use","id":"[^"]*","name":"([A-Za-z]+)"') | ForEach-Object { $_.Groups[1].Value }
  $Meta.tool_uses = @($Names).Count
  $Meta.tools = ($Names | Group-Object | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ','
} catch { $Meta.parse_error = 'client output has no result line' }
# 저장소 밖 접근 검사: 도구 입력(tool_use 의 input)에 금지 경로 문자열이 있는가
$Inputs = [regex]::Matches($Raw, '"type":"tool_use","id":"[^"]*","name":"[A-Za-z]+","input":(\{.*?\})\}') | ForEach-Object { $_.Groups[1].Value }
$Bad = @($Inputs | Where-Object { $_ -match '(?i)strata-lab|configs[\\/]+eval|[\\/]private[\\/]|ref\.patch|test_x3_hidden|strata-x4d[\\/]+_private' })
$Meta.audit = if ($Bad.Count) { "HIT $($Bad.Count): " + (($Bad | Select-Object -First 3) -join ' | ').Substring(0, [math]::Min(300, (($Bad | Select-Object -First 3) -join ' | ').Length)) } else { 'clean' }
[IO.File]::WriteAllText("$Priv\$RunName.meta.json", ($Meta | ConvertTo-Json -Depth 5), $Utf8)

# 4) diff (새 파일 포함) → 채점 (X4 와 같은 x4_grade.py, 결과는 work\x4\results.jsonl)
git -C $Work -c core.autocrlf=false add -A
git -C $Work -c core.autocrlf=false diff --cached HEAD --output="$Priv\$RunName.diff"
"[x4d] $RunName wall ${Wall}s turns $($Meta.num_turns) tools $($Meta.tools) diff $((Get-Item "$Priv\$RunName.diff").Length)B RAM 여유 최소 $RamMin MB audit $($Meta.audit)"
$env:PYTHONUTF8 = '1'
& C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe "$Lab\scripts\bench\x4_grade.py" $Set $Task "$Priv\$RunName.diff" $RunName --client claude-desk --meta "$Priv\$RunName.meta.json"
