# H1 재확인(11-19 사용자 결정, 연속 체인 마지막): H1 단독(paged, reasoning 재전송 없음) X3 6과제(튜닝 3 + 확인 전용 D · E · F) x 5회.
# 대조는 같은 날 채택 확인의 H0 30회(x3c5h0, 17/30 · D · E · F 7/15). 같은 세션 번갈아가 아니므로 '재확인' 이고, 기준을 넘으면
# 다음 체인에서 H0 와 번갈아 정식 확인한다. 접두사는 이 체인 전용(x3c6h1). 끝 표시 '[h1conf] done'.
param([int]$Context = 32768, [int]$Reps = 5)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
function Ensure-Server {
  $h = $null
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if ($h -and $h.loaded -and $h.max_context -eq $Context) { return $h }
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1 | Write-Host
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-h1conf.log" -RedirectStandardError "C:\strata-lab\engine\serve-h1conf.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  return $h
}
"[h1conf] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
$h = Ensure-Server
"[h1conf] ready ctx $($h.max_context) $(Get-Date -Format s)"
$tasks = @('dg_group_names', 'marker_extras', 'version_bump', 'tags_platform_filter', 'metadata_extra_dupes', 'specifier_bounds')
$a = @('--harness', 'H1', '--tool-out', 'paged', '--reasoning-echo', 'none', '--final-turn', 'none')
for ($r = 1; $r -le $Reps; $r++) {
  $null = Ensure-Server
  "[h1conf] rep $r H1 $(Get-Date -Format s)"
  & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks @tasks --prefix x3c6h1 @a --rep-start $r 2>&1 | ForEach-Object { "[h1conf] $_" }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
"[h1conf] done $(Get-Date -Format s)"
