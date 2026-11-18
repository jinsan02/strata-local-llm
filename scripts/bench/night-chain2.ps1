# 밤 체인 2차: 1차('[night] done') 뒤 준비한 코드 · 문서를 커밋하고(실패하면 측정하지 않음) H0 · H2a · H2b · S1T3 을 번갈아 3회.
# WMI 로 띄워 노트북 연결과 무관. 끝 표시 '[night2] done'. 원장 커밋은 하지 않는다(연결 재개 뒤 Claude 가 확인하고 커밋).
param([int]$Context = 32768, [int]$Reps = 3)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
"[night2] waiting for night1 $(Get-Date -Format s)"
$deadline = (Get-Date).AddHours(8)
while ((Get-Date) -lt $deadline) {
  if (Select-String -Path C:\strata-lab\engine\night-chain.log -Pattern '\[night\] done' -Quiet) { break }
  Start-Sleep -Seconds 60
}
if (-not (Select-String -Path C:\strata-lab\engine\night-chain.log -Pattern '\[night\] done' -Quiet)) { "[night2] night1 done 표시 없음, 중단"; exit 1 }
"[night2] night1 finished, commit staged code $(Get-Date -Format s)"
Set-Location C:\strata-lab
& $py -u C:\Users\jinsan\AppData\Local\Temp\x3\v4\commit_v4.py 2>&1 | ForEach-Object { "[night2] $_" }
if ($LASTEXITCODE -ne 0) { "[night2] 커밋 실패 -> 측정하지 않고 종료 $(Get-Date -Format s)"; "[night2] done (aborted)"; exit 1 }
function Ensure-Server {
  $h = $null
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if ($h -and $h.loaded -and $h.max_context -eq $Context) { return $h }
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
  $k = [int]($Context / 1024)
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-night2-ctx${k}k.log" -RedirectStandardError "C:\strata-lab\engine\serve-night2-ctx${k}k.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  return $h
}
$h = Ensure-Server
"[night2] ready ctx $($h.max_context) $(Get-Date -Format s)"
# H0 는 1차의 r1~r3 뒤를 이어 r4~r6 (같은 세션의 대조군)
$arms = @(
  @{n = 'H0';   x = 'x3h0';   s = 'x3sh0';   off = 3; a = @('--harness', 'H0', '--tool-out', 'chars')},
  @{n = 'H2a';  x = 'x3h2a';  s = 'x3sh2a';  off = 0; a = @('--harness', 'H2a', '--tool-out', 'chars', '--reasoning-echo', 'all')},
  @{n = 'H2b';  x = 'x3h2b';  s = 'x3sh2b';  off = 0; a = @('--harness', 'H2b', '--tool-out', 'chars', '--reasoning-echo', 'last')},
  @{n = 'S1T3'; x = 'x3h0t3'; s = 'x3sh0t3'; off = 0; a = @('--harness', 'H0', '--tool-out', 'chars', '--reasoning-budget', '3072', '--settings-id', 'S1T3')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $rs = $r + $arm.off
    $extra = $arm.a
    "[night2] rep $rs $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix $arm.x @extra --rep-start $rs 2>&1 | ForEach-Object { "[night2] $_" }
    & $py -u C:\strata-lab\scripts\bench\run_swe.py --prefix $arm.s @extra --rep-start $rs 2>&1 | ForEach-Object { "[night2] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\user-mode.ps1 | Select-Object -Last 1
"[night2] done $(Get-Date -Format s)"
