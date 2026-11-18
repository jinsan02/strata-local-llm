# 밤 체인 3차: H0(대조) vs H4(강제 마지막 턴에 edit_file 만) 번갈아 3회, X3 navigate 3과제 + SWE 2건.
# 접두사는 이 체인 전용(x3n3h0 · x3h4 …): 다른 체인과 run 폴더를 나누지 않는다(11-19 정정 기록). WMI 로 띄워 노트북 연결과 무관.
# 끝 표시 '[night3] done'. 원장 커밋은 하지 않는다(연결 재개 뒤 Claude 가 확인하고 커밋).
param([int]$Context = 32768, [int]$Reps = 3)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
function Ensure-Server {
  $h = $null
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if ($h -and $h.loaded -and $h.max_context -eq $Context) { return $h }
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
  $k = [int]($Context / 1024)
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-night3-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-night3-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  return $h
}
"[night3] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
$h = Ensure-Server
"[night3] ready ctx $($h.max_context) $(Get-Date -Format s)"
$arms = @(
  @{n = 'H0'; x = 'x3n3h0'; s = 'x3sn3h0'; a = @('--harness', 'H0', '--tool-out', 'chars', '--final-turn', 'none')},
  @{n = 'H4'; x = 'x3h4';   s = 'x3sh4';   a = @('--harness', 'H4', '--tool-out', 'chars', '--final-turn', 'edit')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[night3] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[night3] $_" }
    & $py -u C:\strata-lab\scripts\bench\run_swe.py --prefix $arm.s @extra --rep-start $r 2>&1 | ForEach-Object { "[night3] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[night3] done $(Get-Date -Format s)"
