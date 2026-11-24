# F1 최종 평가 체인 (docs/final-eval-spec-20261124.md). 확정된 운영 설정으로 final_eval 의 검증 통과 과제를 저장소별로 돈다.
# 과제 내용은 출력하지 않는다(과제 ID · 결과 종류만). 끝 표시 [f1] done. WMI 로 띄운다:
#   Invoke-CimMethod Win32_Process Create 'cmd /c powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\bench\f1-chain.ps1 -Engine E3 > C:\strata-lab\engine\f1-chain.log 2>&1'
param([ValidateSet('E2', 'E3')][string]$Engine = 'E3', [int]$Reps = 3, [string]$Prefix = 'f1', [switch]$H10)
$ErrorActionPreference = 'Continue'
$Lab = 'C:\strata-lab'
"[f1] start $(Get-Date -Format s) commit $(git -C $Lab rev-parse --short HEAD) engine $Engine reps $Reps"
foreach ($Repo in 'attrs', 'click', 'dateutil', 'pluggy') {
  $Dir = "$Lab\final_eval\$Repo"
  if (-not (Test-Path $Dir)) { "[f1] $Repo 과제 폴더 없음 - 건너뜀"; continue }
  # 검증 통과 과제만 (final_eval\_validation\<ID>.json 의 pass)
  $Tasks = @(Get-ChildItem $Dir -Directory | Where-Object {
      $v = "$Lab\final_eval\_validation\$($_.Name).json"
      (Test-Path $v) -and ((Get-Content $v -Raw -Encoding utf8 | ConvertFrom-Json).pass -eq $true) } | ForEach-Object { $_.Name })
  "[f1] $Repo 과제 $($Tasks.Count)개"
  if (-not $Tasks.Count) { continue }
  $p = @{ Context = 65536; Reps = $Reps; Only = @('M0'); ForceX3 = $true; Harness = 'H9'; Prefix = $Prefix; EditApply = 'lenient'
          Effort = 'high'; Engine = $Engine; H9 = $true; TaskSet = "final-$Repo"; TaskList = $Tasks }
  if ($H10) { $p.H10 = $true }
  & "$Lab\scripts\bench\g3-chain.ps1" @p 2>&1
  "[f1] $Repo end $(Get-Date -Format s)"
}
"[f1] done $(Get-Date -Format s)"
