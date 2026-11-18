# 낮 모드 (로컬 LLM): cleanup.ps1 + 추가 앱 종료 + 불필요 서비스 '중지'. 프로그램 삭제 · 시작 유형 변경 없음.
# 관리자 권한 필요 (서비스 중지). 되돌리기: user-mode.ps1 (중지한 서비스만 다시 시작) 또는 재부팅.
# 남기는 것: KakaoTalk, Tailscale, sshd, Defender, 오디오, NVIDIA 드라이버 서비스, ASUS 팬 제어, TCube, Claude Cowork VM (사용자 결정 11-18)
param([string]$LogDir = 'C:\strata-lab\env')
$ErrorActionPreference = 'Continue'
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\cleanup.ps1 -LogDir $LogDir | Select-Object -Last 1

$apps = 'ASUS MB Manager', 'NGenuity2Helper', 'PhoneExperienceHost', 'RadeonSoftware', 'AMDRSServ', 'OfficeClickToRun'
$services = 'XboxService', 'GamingServices', 'GamingServicesNet', 'GameInputRedistService', 'ClickToRunSvc',
            'LGHUBUpdaterService', 'KollusSvr', 'CodexSandboxService.OpenAI.Codex', 'WSearch'

$os = Get-CimInstance Win32_OperatingSystem
$before = "{0:N2}" -f ($os.FreePhysicalMemory / 1MB)
$killed = foreach ($n in $apps) { $p = Get-Process -Name $n -ErrorAction SilentlyContinue; if ($p) { $p | Stop-Process -Force -ErrorAction SilentlyContinue; "$n x$($p.Count)" } }
$stopped = foreach ($s in $services) {
  $svc = Get-Service -Name $s -ErrorAction SilentlyContinue
  if ($svc -and $svc.Status -eq 'Running') {
    try { Stop-Service -Name $s -Force -ErrorAction Stop; $s } catch { "$s(실패: $($_.Exception.Message))" }
  }
}
# user-mode.ps1 이 정확히 이것만 다시 켜도록 기록
@{ ts = (Get-Date -Format s); stopped = @($stopped | Where-Object { $_ -notmatch '실패' }) } | ConvertTo-Json | Out-File (Join-Path $LogDir 'llm-mode-state.json') -Encoding utf8
Start-Sleep -Seconds 3
$os = Get-CimInstance Win32_OperatingSystem
$line = "{0} llm-mode: FreeRAM {1} -> {2:N2} GB; apps: {3}; services: {4}" -f (Get-Date -Format s), $before, ($os.FreePhysicalMemory / 1MB), ($killed -join ', '), ($stopped -join ', ')
$line | Tee-Object -FilePath (Join-Path $LogDir 'mode.log') -Append
