# 밤 모드 (사용자): STRATA 서버를 끄고, llm-mode.ps1 이 중지한 서비스만 다시 시작한다. 앱은 사용자가 열 때 뜬다.
# 관리자 권한 필요. 시작 프로그램 해제(Discord 등 7개)는 그대로 둔다 — 되돌리려면 env\startup-backup*.reg.
param([string]$LogDir = 'C:\strata-lab\env', [switch]$KeepServer)
$ErrorActionPreference = 'Continue'
if (-not $KeepServer) { & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null }
$state = Join-Path $LogDir 'llm-mode-state.json'
$started = @()
if (Test-Path $state) {
  foreach ($s in (Get-Content $state -Raw -Encoding UTF8 | ConvertFrom-Json).stopped) {
    try { Start-Service -Name $s -ErrorAction Stop; $started += $s } catch { $started += "$s(실패)" }
  }
}
$os = Get-CimInstance Win32_OperatingSystem
$line = "{0} user-mode: server {1}; services: {2}; FreeRAM {3:N2} GB" -f (Get-Date -Format s), $(if ($KeepServer) { 'kept' } else { 'stopped' }), ($started -join ', '), ($os.FreePhysicalMemory / 1MB)
$line | Tee-Object -FilePath (Join-Path $LogDir 'mode.log') -Append
