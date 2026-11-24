# X4b 일괄 (본체, 테스트 실행 허용): X4 A 와 같은 8과제 x 2회, 실행 이름 x4b_<과제>_r<회>.
# ssh 를 끊어도 살도록 WMI 로 띄운다:
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\local\x4d-batch.ps1 -Launch
# 로그 C:\strata-lab\work\x4\x4b-batch.log, 끝 표시 [x4b] done. 서버는 strata-up.ps1 로 미리 띄운다.
# 과제마다 별도 powershell 프로세스(같은 세션에서 2>&1 로 합치면 stderr 가 ErrorRecord 가 되어 멈춘다).
# 일부만: -Only "dg_group_names:2,y1_version_postdev_order:2" (11-24 네트워크 차단 뒤 남은 5건은 -Prefix x4bf)
param([switch]$Launch, [string]$Prefix = 'x4b', [string]$Only = '')
$Log = "C:\strata-lab\work\x4\$Prefix-batch.log"
if ($Launch) {
  $cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command `"& '$PSCommandPath' -Prefix $Prefix -Only '$Only' *>&1 | Out-File -FilePath $Log -Encoding utf8`""
  $r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $cmd; CurrentDirectory = 'C:\strata-lab' }
  "[x4b] launch pid $($r.ProcessId) rc $($r.ReturnValue) log $Log"
  return
}
$Jobs = @(
  @('y', 'y2_wheel_build_number', 1), @('x3', 'version_bump', 1), @('x3', 'tags_platform_filter', 1), @('x3', 'dg_group_names', 1),
  @('y', 'y1_version_postdev_order', 1), @('y', 'y4_refactor_filename_version', 1), @('y', 'y5_session_cookie_max_age', 1), @('y', 'y6_config_require', 1),
  @('y', 'y2_wheel_build_number', 2), @('x3', 'version_bump', 2), @('x3', 'tags_platform_filter', 2), @('x3', 'dg_group_names', 2),
  @('y', 'y1_version_postdev_order', 2), @('y', 'y4_refactor_filename_version', 2), @('y', 'y5_session_cookie_max_age', 2), @('y', 'y6_config_require', 2)
)
if ($Only) { $Want = $Only -split ","; $Jobs = @($Jobs | Where-Object { "$($_[1]):$($_[2])" -in $Want }) }
"[x4b] jobs $($Jobs.Count) prefix $Prefix"
$Task = Join-Path $PSScriptRoot 'x4d-task.ps1'
"[x4b] start $(Get-Date -Format s)"
foreach ($J in $Jobs) {
  "[x4b] >>> $($J[0]) $($J[1]) r$($J[2]) $(Get-Date -Format s)"
  $Out = cmd /c "powershell -NoProfile -ExecutionPolicy Bypass -File `"$Task`" -Set $($J[0]) -Task $($J[1]) -Rep $($J[2]) -Prefix $Prefix 2>&1"
  $Out | Where-Object { "$_" -notmatch 'LF will be replaced' }
  "[x4b] rc $LASTEXITCODE"
}
"[x4b] done $(Get-Date -Format s)"
