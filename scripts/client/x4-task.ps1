# X4 (노트북): 실제 클라이언트(Claude Code CLI)로 X3 · Y 과제 하나를 풀고, 결과 diff 를 본체에서 채점한다.
# 서버는 본체에서 미리 띄운다: ssh desktop-5070 "powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\launch_serve.ps1"
# 측정 체인이 도는 동안에는 쓰지 않는다(같은 GPU). 숨은 테스트 · 참조 패치는 노트북으로 가져오지 않는다(채점은 본체 x4_grade.py).
#
# 예:  .\x4-task.ps1 -Set y -Task y2_wheel_build_number -Rep 1
#      .\x4-task.ps1 -Set x3 -Task version_bump -DryRun        # 서버 · 모델 없이 준비 · 채점 경로만 확인
param([ValidateSet('x3', 'y')][string]$Set = 'y', [Parameter(Mandatory = $true)][string]$Task, [int]$Rep = 1,
      [int]$MaxTurns = 40, [string]$Prefix = 'x4c', [switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Home4 = Join-Path $env:USERPROFILE 'strata-x4'
$Cache = Join-Path $Home4 '_cache'
$Priv = Join-Path $Home4 '_private'      # 작업 폴더 밖: 지시문 원본 · 클라이언트 출력 · diff
$RunName = "${Prefix}_${Task}_r$Rep"
$Work = Join-Path $Home4 $RunName
$SetDir = if ($Set -eq 'y') { 'y-set' } else { 'x3-packaging' }
$Remote = "C:/strata-lab/configs/eval/$SetDir/$Task"
New-Item -ItemType Directory -Force $Cache, $Priv | Out-Null
$Utf8 = New-Object System.Text.UTF8Encoding($false)

# 1) 과제 정보: task.json · prompt.md 만 (private 는 setup_patch 만, 적용 직후 지운다)
scp -q "desktop-5070:$Remote/task.json" "$Priv/$RunName.task.json"
scp -q "desktop-5070:$Remote/prompt.md" "$Priv/$RunName.prompt.md"
$Cfg = Get-Content "$Priv/$RunName.task.json" -Raw -Encoding utf8 | ConvertFrom-Json
$RepoName = if ($Cfg.repo) { $Cfg.repo } else { 'packaging' }
$Commit = @{ packaging = '6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc'; flask = '7ee9ceb71e868944a46e1ff00b506772a53a4f1d' }[$RepoName]
$Label = @{ packaging = 'pypa/packaging'; flask = 'pallets/flask' }[$RepoName]

# 2) 작업 복사본: 본체가 만든 git bundle 에서 고정 커밋, setup_patch 는 커밋으로 넣는다
$Bundle = Join-Path $Cache "$RepoName.bundle"
if (-not (Test-Path $Bundle)) { scp -q "desktop-5070:C:/strata-lab/work/x4/bundles/$RepoName.bundle" $Bundle }
if (Test-Path $Work) { Remove-Item -Recurse -Force $Work }
git clone -q --no-checkout $Bundle $Work
git -C $Work -c core.autocrlf=false checkout -q --detach $Commit
if ($Cfg.setup_patch) {
  $SetupFile = "$Priv/$RunName.setup.patch"
  scp -q "desktop-5070:$Remote/$($Cfg.setup_patch)" $SetupFile
  git -C $Work apply $SetupFile
  Remove-Item $SetupFile
}
git -C $Work -c core.autocrlf=false add -A
git -C $Work -c user.name=x4 -c user.email=x4@localhost commit -q --allow-empty -m setup

# 3) 지시문: 과제 원문 + 환경 안내(노트북에는 Python 이 없어 테스트를 돌릴 수 없다)
$Allow = @($Cfg.write_allow)
$Rule = if ($Allow.Count -and $Allow[0]) { "테스트 파일은 고치지 마라. 새로 만들 파일: $($Allow -join ', ')" } else { '테스트 파일은 고치지 마라.' }
$Note = "너는 $Label 저장소(현재 폴더, 고정 커밋)에서 작업한다. 이 환경에는 Python 이 없어 테스트를 돌릴 수 없으니, 코드를 읽고 Edit · Write 도구로 직접 고쳐라. $Rule"
$PromptFile = "$Priv/$RunName.prompt.txt"
[IO.File]::WriteAllText($PromptFile, (Get-Content "$Priv/$RunName.prompt.md" -Raw -Encoding utf8) + [Environment]::NewLine + [Environment]::NewLine + $Note, $Utf8)

# 4) 클라이언트 실행 (개인 설정 · 훅 · 메모리 · MCP 를 빼고, 셸 도구 없이)
$ClientArgs = @('-p', '--output-format', 'stream-json', '--verbose', '--max-turns', "$MaxTurns", '--bare', '--setting-sources', 'project', '--no-session-persistence',
                '--permission-mode', 'acceptEdits', '--allowedTools', 'Read,Edit,Write,Glob,Grep', '--disallowedTools', 'Bash,WebFetch,WebSearch,Task')
$env:STRATA_CONTEXT = '65536'
$T0 = Get-Date
if ($DryRun) {
  "[x4] DryRun: $Work 준비 끝. 실행할 명령: claude-local.ps1 -PromptFile $PromptFile $($ClientArgs -join ' ')"
  $Raw = '{"dry_run": true}'
} else {
  Push-Location $Work
  [Console]::OutputEncoding = $Utf8   # claude 의 UTF-8 출력을 콘솔 코드 페이지(cp949)로 잘못 읽지 않게 (11-24 첫 실행 결과 글자가 깨짐)
  try { $Raw = (& (Join-Path $PSScriptRoot 'claude-local.ps1') -PromptFile $PromptFile @ClientArgs) -join [Environment]::NewLine }
  finally { Pop-Location }
}
$Wall = [math]::Round(((Get-Date) - $T0).TotalSeconds, 1)
[IO.File]::WriteAllText("$Priv/$RunName.client.jsonl", "$Raw", $Utf8)   # stream-json: 도구 호출 하나하나가 남는다(분석용)
$Meta = @{ wall_s = $Wall; client = 'claude-code'; client_version = ((claude --version) -join ' '); max_turns = $MaxTurns; dry_run = [bool]$DryRun }
try {
  $Last = ($Raw -split [Environment]::NewLine | Where-Object { $_ -match '"type":"result"' } | Select-Object -Last 1)
  $J = $Last | ConvertFrom-Json
  $Meta.num_turns = $J.num_turns; $Meta.is_error = $J.is_error; $Meta.duration_ms = $J.duration_ms; $Meta.usage = $J.usage
  $Meta.result_head = "$($J.result)".Substring(0, [math]::Min(400, "$($J.result)".Length))
  $Names = [regex]::Matches($Raw, '"type":"tool_use","id":"[^"]*","name":"([A-Za-z]+)"') | ForEach-Object { $_.Groups[1].Value }
  $Meta.tool_uses = @($Names).Count
  $Meta.tools = ($Names | Group-Object | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ','
} catch { $Meta.parse_error = 'client output has no result line' }
[IO.File]::WriteAllText("$Priv/$RunName.meta.json", ($Meta | ConvertTo-Json -Depth 5), $Utf8)

# 5) diff (새 파일 포함) → 본체 채점
git -C $Work -c core.autocrlf=false add -A
git -C $Work -c core.autocrlf=false diff --cached HEAD --output="$Priv/$RunName.diff"
ssh desktop-5070 "if not exist C:\strata-lab\work\x4\in mkdir C:\strata-lab\work\x4\in" | Out-Null
scp -q "$Priv/$RunName.diff" "$Priv/$RunName.meta.json" "desktop-5070:C:/strata-lab/work/x4/in/"
"[x4] $RunName wall ${Wall}s turns $($Meta.num_turns) diff $((Get-Item "$Priv/$RunName.diff").Length)B"
ssh desktop-5070 "set PYTHONUTF8=1&& C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe C:\strata-lab\scripts\bench\x4_grade.py $Set $Task C:\strata-lab\work\x4\in\$RunName.diff $RunName --client claude --meta C:\strata-lab\work\x4\in\$RunName.meta.json"
