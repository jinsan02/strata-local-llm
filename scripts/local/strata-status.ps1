# STRATA 서버 상태: 프로세스 · 듣는 주소 · /v1/models · RAM · GPU. 키 값은 출력하지 않는다.
$ErrorActionPreference = 'Continue'
$srv = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'serve\\server\.py' }
$eng = Get-Process strata -ErrorAction SilentlyContinue
"server.py : $(if ($srv) { 'pid ' + (@($srv.ProcessId) -join ',') } else { '없음' })"
"strata.exe: $(if ($eng) { 'pid ' + (@($eng.Id) -join ',') + ', RAM ' + [int](($eng | Measure-Object WS -Sum).Sum / 1MB) + ' MB' } else { '없음' })"
$ls = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
$addr = @(@($ls | ForEach-Object { $_.LocalAddress }) | Select-Object -Unique)   # @() 필수: 하나면 문자열이 되어 [0] 이 첫 글자가 된다
"듣는 주소 : $(if ($addr) { ($addr | ForEach-Object { "${_}:8080" }) -join ', ' } else { '없음' })"
if ($addr) {
  $key = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
  $h = if ($addr[0] -in @('0.0.0.0', '::')) { '127.0.0.1' } else { $addr[0] }
  try {
    $m = Invoke-RestMethod -Uri "http://${h}:8080/v1/models" -Headers @{ Authorization = "Bearer $key" } -TimeoutSec 5
    "응답      : $($m.data[0].id)"
  } catch { "응답      : 실패 ($($_.Exception.Message))" }
  try { $hl = Invoke-RestMethod -Uri "http://${h}:8080/health" -TimeoutSec 5; "health    : $($hl | ConvertTo-Json -Compress -Depth 3)" } catch { }
}
$os = Get-CimInstance Win32_OperatingSystem
"RAM 여유  : $([int]($os.FreePhysicalMemory / 1024)) MB / $([int]($os.TotalVisibleMemorySize / 1024)) MB"
$g = & nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader 2>$null
if ($g) { "GPU       : $g" }
