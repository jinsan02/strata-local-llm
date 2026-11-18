# STRATA 측정 전 백그라운드 정리 (프로그램 삭제 없음, 프로세스 종료만)
param([string]$LogDir = 'C:\strata-lab\env')
New-Item -ItemType Directory -Force $LogDir | Out-Null
function Snap($tag) {
  $os = Get-CimInstance Win32_OperatingSystem
  $commit = (Get-Counter '\Memory\Committed Bytes').CounterSamples[0].CookedValue
  $gpu = (nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits).Trim()
  "{0} {1}: FreeRAM {2:N2} GB, Committed {3:N2} GB, GPU used {4} MiB" -f (Get-Date -Format s), $tag, ($os.FreePhysicalMemory/1MB), ($commit/1GB), $gpu
}
$names = 'Discord','steam','steamwebhelper','NexonPlug','RiotClientServices','RiotClientUx','RiotClientCrashHandler',
         'ms-teams','msteams','copilotapp','copilotapphost','MythCool','NVIDIA Overlay','RadeonSoftware','AMDRSSrcExt',
         'lghub_system_tray','lghub','PhoneExperienceHost','ChatGPT','codex','codex-computer-use-swift','SOOPLiveLauncher'
$before = Snap 'before'
$killed = @()
foreach ($n in $names) {
  $p = Get-Process -Name $n -ErrorAction SilentlyContinue
  if ($p) { $p | Stop-Process -Force -ErrorAction SilentlyContinue; $killed += "$n x$($p.Count)" }
}
Start-Sleep -Seconds 5
$after = Snap 'after'
$out = @($before, "killed: $($killed -join ', ')", $after)
$out | Tee-Object -FilePath (Join-Path $LogDir 'cleanup.log') -Append
