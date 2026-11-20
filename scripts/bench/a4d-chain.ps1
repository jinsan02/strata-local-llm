# A4 원인 확인 (11-20 사용자: H2a 끝나면 바로). STRATA_DEBUG=1 로 서버가 응답마다 raw 텍스트 · raw ids 를 남기게 하고,
#   H2a + card-coding 으로 version_bump · dg_group_names x 3회(seed 42~44). 접두사 x3a4d. 재사용 0 턴의 직전 raw ids 를 다음 프롬프트 재인코딩과 비교한다.
# 설정 고정 · 슬롯 확인 · nvidia-smi 는 s1-chain 과 같다. 끝 표시 '[a4d] done'. 코드 변경 없음(work\stage 에서 실행했고 기록을 위해 여기에 둠).
# STRATA_DEBUG 는 serve-ctx 가 STRATA_* 를 지우므로 -EnvSet 으로 넘긴다(server.py 가 응답마다 [strata] raw: / raw ids: 를 남김).
param([int]$Context = 32768, [int]$Reps = 3, [int]$ExpectSlots = 63)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$engLog = "C:\strata-lab\engine\strata-qwen36-ctx$Context-a4d.log"
function Slots {
  if (-not (Test-Path $engLog)) { return -1 }
  $m = Select-String -Path $engLog -Pattern 'hybrid experts: (\d+) of 256' | Select-Object -Last 1
  if ($m) { return [int]$m.Matches[0].Groups[1].Value } else { return -1 }
}
function Start-Server {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context -Tag a4d -EnvSet STRATA_DEBUG=1" `
    -RedirectStandardOutput "C:\strata-lab\engine\serve-a4d.log" -RedirectStandardError "C:\strata-lab\engine\serve-a4d.err" -WindowStyle Hidden
  $h = $null
  for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 5
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
  }
  return $h
}
function Ensure-Server {
  $h = $null
  try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3 } catch {}
  if ($h -and $h.loaded -and $h.max_context -eq $Context) { return $h }
  for ($try = 1; $try -le 2; $try++) {
    $vram = (& nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits) -join ''
    "[a4d] server start try $try (GPU used before $vram MiB) $(Get-Date -Format s)"
    $h = Start-Server
    $s = Slots
    "[a4d] server loaded=$($h.loaded) slots=$s (expect $ExpectSlots)"
    if ($s -eq $ExpectSlots) { break }
    "[a4d] 경고: 슬롯 수가 다름 - 다시 띄움"
  }
  return $h
}
"[a4d] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
"[a4d] power $((powercfg /getactivescheme) -join ' ')"
$gpu = Start-Process nvidia-smi -ArgumentList '--query-gpu=timestamp,temperature.gpu,clocks.sm,clocks.mem,power.draw,memory.used,clocks_event_reasons.active --format=csv -l 60 -f C:\strata-lab\engine\gpu-a4d.csv' -WindowStyle Hidden -PassThru
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$h = Ensure-Server
"[a4d] ready ctx $($h.max_context) $(Get-Date -Format s)"
$tasks = @('version_bump', 'dg_group_names')
$hb = @('--harness', 'H2a', '--tool-out', 'chars', '--reasoning-echo', 'all', '--final-turn', 'none', '--seed-per-rep')
$arms = @(
  @{n = 'D'; x = 'x3a4d'; a = $hb + @('--sampling', 'card-coding')}
)
for ($r = 1; $r -le $Reps; $r++) {
  foreach ($arm in $arms) {
    $null = Ensure-Server
    $extra = $arm.a
    "[a4d] rep $r $($arm.n) $(Get-Date -Format s)"
    & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks @tasks --prefix $arm.x @extra --rep-start $r 2>&1 | ForEach-Object { "[a4d] $_" }
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
if ($gpu -and -not $gpu.HasExited) { Stop-Process -Id $gpu.Id -Force }
"[a4d] done $(Get-Date -Format s)"
