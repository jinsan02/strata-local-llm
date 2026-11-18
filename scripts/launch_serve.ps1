# 운영용 STRATA 서버를 ssh 작업 객체 밖(WMI)에서 띄운다 — ssh 를 끊어도 산다 (T-012).
# 로컬 LLM 을 주 에이전트(노트북 claude-local · codex-local)나 워커(scripts/worker)로 쓸 때 이것으로 띄운다.
# 키는 실행 시 .secrets 에서 읽는다(명령줄 · 로그에 값이 남지 않게).
#
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\launch_serve.ps1                 # 32K, Tailscale(노트북 · 본체 워커 둘 다)
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\launch_serve.ps1 -Host_ 127.0.0.1 # 본체 안에서만
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\launch_serve.ps1 -LlmMode         # 측정급: 백그라운드 정리 · 전원 고정 뒤 띄움
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop               # 내리기 (밤에는 user-mode.ps1)
param(
  [int]$Context = 32768,
  [string]$Host_ = '100.121.174.83',
  [switch]$LlmMode,
  [int]$WaitSec = 180
)
$lab = 'C:\strata-lab'
$log = "$lab\engine\serve-detached.log"
$pre = if ($LlmMode) { "& $lab\scripts\llm-mode.ps1; " } else { '' }
$inner = "$pre`$env:STRATA_API_KEY = (Get-Content $lab\.secrets\strata-api-key.txt -Raw).Trim(); " +
         "& $lab\scripts\serve-ctx.ps1 -Context $Context -Host_ $Host_ *>&1 | Out-File -FilePath $log -Encoding utf8"
$cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command `"$inner`""
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $cmd; CurrentDirectory = $lab}
"[launch] pid $($r.ProcessId) rc $($r.ReturnValue)  (context $Context, host $Host_, log $log)"
if ($r.ReturnValue -ne 0) { exit 1 }
$key = (Get-Content "$lab\.secrets\strata-api-key.txt" -Raw).Trim()
$t0 = Get-Date
while (((Get-Date) - $t0).TotalSeconds -lt $WaitSec) {
  Start-Sleep -Seconds 5
  try {
    $m = Invoke-RestMethod -Uri "http://$($Host_):8080/v1/models" -Headers @{Authorization = "Bearer $key"} -TimeoutSec 5
    "[launch] 준비됨 $([int]((Get-Date) - $t0).TotalSeconds)초: $($m.data[0].id) @ http://$($Host_):8080"
    exit 0
  } catch { }
}
"[launch] $WaitSec 초 안에 응답 없음 — $log 확인"
exit 1
