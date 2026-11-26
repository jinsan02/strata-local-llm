# STRATA 세션 시작 점검: 작업을 시작하기 전에 한 번 돌린다. 읽기만 하고 아무것도 바꾸지 않는다.
# git 상태 · 안 올린 커밋 · 작업 트리 · 도는 측정/워커 · 서버 · RAM/GPU/디스크 · 원장 마지막 줄 · STATE '지금'.
# 키 값은 출력하지 않는다(서버 확인은 strata-status.ps1 이 한다).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\local\session-start.ps1 [-StateLines 12] [-Fetch]
param([int]$StateLines = 12, [switch]$Fetch)
$ErrorActionPreference = 'Continue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$warn = New-Object System.Collections.Generic.List[string]
function Section($t) { ''; "== $t ==" }
function Invoke-RepoGit { & git.exe -C $root @args 2>$null }   # 이름을 Git 으로 두면 PowerShell 은 대소문자를 안 가려 자기 자신을 부른다

Section 'git'
$branch = Invoke-RepoGit rev-parse --abbrev-ref HEAD
"브랜치    : $branch"
if ($branch -ne 'main') { $warn.Add("main 이 아닌 브랜치($branch)다. 다른 세션이 쓰는 중인지 확인") }
$st = @(Invoke-RepoGit status --porcelain)
$mod = @($st | Where-Object { $_ -notmatch '^\?\?' }).Count
$unt = @($st | Where-Object { $_ -match '^\?\?' }).Count
"변경      : 추적 파일 $mod 개 · 새 파일 $unt 개"
if ($mod) { $st | Where-Object { $_ -notmatch '^\?\?' } | Select-Object -First 8 | ForEach-Object { "            $_" } }
if ($Fetch) { Invoke-RepoGit fetch -q origin | Out-Null }
$up = Invoke-RepoGit rev-parse --abbrev-ref '@{u}'
if (-not $up) { $up = 'origin/main' }
$lr = (Invoke-RepoGit rev-list --left-right --count "$up...HEAD") -split '\s+'
if ($lr.Count -eq 2) {
  "기준 $up : 뒤 $($lr[0]) · 앞 $($lr[1])$(if (-not $Fetch) { ' (마지막 fetch 기준, -Fetch 로 갱신)' })"
  if ([int]$lr[1] -gt 0) { $warn.Add("push 안 한 커밋 $($lr[1])개 ($branch → $up). push 는 사용자 승인 뒤") }
}
'최근 커밋 :'
Invoke-RepoGit log --oneline -5 | ForEach-Object { "            $_" }
$wts = @(Invoke-RepoGit worktree list) | Where-Object { $_ }
if ($wts.Count -gt 1) {
  "작업 트리 : $($wts.Count)개"
  $wts | ForEach-Object { "            $_" }
}
$ww = Join-Path $root 'work\worker'
if (Test-Path $ww) {
  $left = @(Get-ChildItem $ww -Directory | Where-Object { $_.Name -ne 'logs' -and $_.Name -notlike '_*' })
  if ($left.Count) { "워커 트리 : $($left.Count)개 남음 ($(($left | Select-Object -First 5 | ForEach-Object Name) -join ', '))"; $warn.Add("워커 작업 트리 $($left.Count)개가 남아 있다(discard_worktree)") }
}

Section '도는 작업'
$pat = 'night-chain|matrix-[a-z0-9]+\.ps1|-chain\.ps1|launch_[a-z0-9]+\.ps1|x4d-batch|run_(x3|swe|bench|coding)\.py|strata_worker\.py'
$procs = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe' or Name='pwsh.exe' or Name='python.exe'" |
  Where-Object { $_.CommandLine -match $pat -and $_.CommandLine -notmatch 'session-start\.ps1' })
if ($procs.Count) {
  $procs | ForEach-Object { "pid $($_.ProcessId): $($_.CommandLine.Substring(0, [Math]::Min(150, $_.CommandLine.Length)))" }
  $warn.Add("측정 · 워커 프로세스 $($procs.Count)개가 돈다. 추적 파일을 고치지 말고 work\stage 에서 준비")
} else { '측정 체인 · 러너 · 워커: 없음' }
$lock = Join-Path $root 'work\worker\busy.lock'
if (Test-Path $lock) { "워커 잠금 : 있음 ($((Get-Content $lock -Raw).Trim()))"; $warn.Add('워커 busy.lock 이 있다') }

Section '서버 · 자원'
& (Join-Path $PSScriptRoot 'strata-status.ps1')
$c = Get-PSDrive C -ErrorAction SilentlyContinue
if ($c) { "C: 여유   : $([int]($c.Free / 1GB)) GB" }

Section '원장 마지막 줄'
$led = Join-Path $root 'experiments\LEDGER.tsv'
if (Test-Path $led) {
  $lines = @(Get-Content $led -Encoding UTF8)
  $h = $lines[0] -split "`t"; $last = $lines[-1] -split "`t"
  $ri = [array]::IndexOf($h, 'run_id'); $ti = [array]::IndexOf($h, 'ts_utc')
  "$($lines.Count - 1)행 · 마지막 $(if ($ri -ge 0) { $last[$ri] }) ($(if ($ti -ge 0) { $last[$ti] }))"
}

Section "STATE '지금' (앞 $StateLines 줄)"
$sp = Join-Path $root 'STATE.md'
if (Test-Path $sp) {
  $s = @(Get-Content $sp -Encoding UTF8)
  $i = [array]::IndexOf($s, '## 지금')
  if ($i -ge 0) {
    $s[($i + 1)..([Math]::Min($s.Count - 1, $i + $StateLines))] | Where-Object { $_.Trim() } |
      ForEach-Object { if ($_.Length -gt 220) { $_.Substring(0, 220) + ' …' } else { $_ } }
  }
}

Section '확인할 것'
if ($warn.Count) { $warn | ForEach-Object { "- $_" } } else { '- 없음. 시작해도 된다' }
