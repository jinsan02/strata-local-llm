# 체인 5차 = 채택 확인: H0(대조) vs H3(H1 + H2a) 번갈아 5회, X3 navigate 6과제(기존 3 + 확인 전용 D · E · F). SWE 는 뺀다(건전성용).
# 기준(11-19 사용자 승인): 30회 통과 H0 대비 -2 이내 · 회귀 실패 증가 없음 · D · E · F 15회 -1 이내, 그다음 시간 · 새로 읽은 입력.
# 접두사는 이 체인 전용(x3c5h0 · x3c5h3): 다른 체인과 run 폴더를 나누지 않는다(11-19 정정 기록). WMI 로 띄워 노트북 연결과 무관.
# 끝 표시 '[night5] done'. 원장 커밋은 하지 않는다(연결 재개 뒤 Claude 가 확인하고 커밋).
param([int]$Context = 32768, [int]$Reps = 5)
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
    -RedirectStandardOutput "C:\strata-lab\engine\serve-night5-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-night5-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  return $h
}
"[night5] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
$h = Ensure-Server
"[night5] ready ctx $($h.max_context) $(Get-Date -Format s)"
$tasks = @('dg_group_names', 'marker_extras', 'version_bump', 'tags_platform_filter', 'metadata_extra_dupes', 'specifier_bounds')
$arms = @(
  @{n = 'H0'; x = 'x3c5h0'; a = @('--harness', 'H0', '--tool-out', 'chars', '--reasoning-echo', 'none', '--final-turn', 'none')},
  @{n = 'H3'; x = 'x3c5h3'; a = @('--harness', 'H3', '--tool-out', 'paged', '--reasoning-echo', 'all', '--final-turn', 'none')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[night5] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks @tasks --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[night5] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[night5] done $(Get-Date -Format s)"
