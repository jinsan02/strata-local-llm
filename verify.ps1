# 커밋 전 전체 검증 — 훅 테스트 → 원장 무결성 → push 안 한 커밋의 메시지 규칙
$ErrorActionPreference = 'Continue'
Set-Location $PSScriptRoot
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }
$fail = 0

Write-Host '== 훅 단위 테스트'
& $py -m pytest tests -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { $fail = 1 }

Write-Host '== 원장 무결성'
& $py tools\validate_ledger.py
if ($LASTEXITCODE -ne 0) { $fail = 1 } else { Write-Host '   통과' }

Write-Host '== push 안 한 커밋의 메시지'
$upstream = git rev-parse --abbrev-ref '@{u}' 2>$null
$range = if ($upstream) { "$upstream..HEAD" } else { 'HEAD' }
$tmp = Join-Path $env:TEMP 'verify-commit-msg.txt'
$shas = git rev-list $range 2>$null
if (-not $shas) { Write-Host '   새 커밋 없음' }
foreach ($sha in $shas) {
  git log -1 --format=%B $sha | Out-File -Encoding utf8 $tmp
  Write-Host "   $(git log -1 --format='%h %s' $sha)"
  & $py tools\check_commit_msg.py $tmp
  if ($LASTEXITCODE -ne 0) { $fail = 1 }
}

if ($fail) { Write-Host "`n검증 실패" -ForegroundColor Red; exit 1 }
Write-Host "`n검증 통과" -ForegroundColor Green
