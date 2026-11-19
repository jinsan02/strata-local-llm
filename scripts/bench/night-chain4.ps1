# 체인 4차: H0(대조) vs H3(= H1 도구 응답 페이지 나누기 + H2a reasoning 전 턴 재전송) 번갈아 3회, X3 navigate 3과제 + SWE 2건.
# H4 는 11-19 A/B 에서 채택하지 않아 빠진다. 접두사는 이 체인 전용(x3n4h0 · x3h3 …): 다른 체인과 run 폴더를 나누지 않는다(11-19 정정 기록). WMI 로 띄워 노트북 연결과 무관.
# 끝 표시 '[night4] done'. 원장 커밋은 하지 않는다(연결 재개 뒤 Claude 가 확인하고 커밋).
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
    -RedirectStandardOutput "C:\strata-lab\engine\serve-night4-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-night4-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  return $h
}
"[night4] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
$h = Ensure-Server
"[night4] ready ctx $($h.max_context) $(Get-Date -Format s)"
$arms = @(
  @{n = 'H0'; x = 'x3n4h0'; s = 'x3sn4h0'; a = @('--harness', 'H0', '--tool-out', 'chars', '--reasoning-echo', 'none', '--final-turn', 'none')},
  @{n = 'H3'; x = 'x3h3';   s = 'x3sh3';   a = @('--harness', 'H3', '--tool-out', 'paged', '--reasoning-echo', 'all', '--final-turn', 'none')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[night4] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[night4] $_" }
    & $py -u C:\strata-lab\scripts\bench\run_swe.py --prefix $arm.s @extra --rep-start $r 2>&1 | ForEach-Object { "[night4] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[night4] done $(Get-Date -Format s)"
