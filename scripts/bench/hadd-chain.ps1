# 하네스 추가 후보 A/B: 기준 하네스(B) 하나를 대조군으로 공유하고 후보를 하나씩 더한 팔과 번갈아 돈다(밤 체인 2차와 같은 방식).
#   B     : 기준(채택 확인 결과로 정함, -BaseArgs)
#   B+H6  : --edit-hint on       (edit_file 0회 일치 때 가장 비슷한 원문)
#   B+C1  : --reread-guard on    (같은 범위 · 같은 내용 재읽기는 안내만)
#   B+RT  : --run-tests on       (공개 테스트 도구, Q15)
# X3 튜닝용 3과제만(확인 전용 D · E · F 는 쓰지 않음), 4회. 판정(11-19 사용자 승인): 정확도 우선, 대조 대비 통과 -1 이내 · 회귀 증가 없음, 그다음 시간 · 입력.
# 접두사는 이 체인 전용(x3a6b · x3a6e · x3a6r · x3a6t). 끝 표시 '[hadd] done'.
param([string]$BaseName = 'H0', [string]$BaseArgs = '--harness H0 --tool-out chars --reasoning-echo none --final-turn none', [int]$Reps = 4, [int]$Context = 32768)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
function Ensure-Server {
  $h = $null
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if ($h -and $h.loaded -and $h.max_context -eq $Context) { return $h }
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1 | Write-Host
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-hadd.log" -RedirectStandardError "C:\strata-lab\engine\serve-hadd.err" -WindowStyle Hidden
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  return $h
}
$base = $BaseArgs -split '\s+' | Where-Object { $_ }
$arms = @(
  @{n = "$BaseName";     x = 'x3a6b'; a = $base},
  @{n = "$BaseName+H6";  x = 'x3a6e'; a = $base + @('--edit-hint', 'on')},
  @{n = "$BaseName+C1";  x = 'x3a6r'; a = $base + @('--reread-guard', 'on')},
  @{n = "$BaseName+RT";  x = 'x3a6t'; a = $base + @('--run-tests', 'on')}
)
"[hadd] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD) base '$BaseArgs'"
$h = Ensure-Server
"[hadd] ready ctx $($h.max_context) $(Get-Date -Format s)"
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[hadd] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[hadd] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
"[hadd] done $(Get-Date -Format s)"
