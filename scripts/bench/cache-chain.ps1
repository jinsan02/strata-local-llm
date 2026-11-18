# 대화 캐시 A/B (T-013 원인 가설, 11-19 첫 작업): --conversation-cache-mib 없음(지금) · 512 · 1024 를 차례로.
# 조건마다 서버를 새로 띄워 cache_ab.py(후속 턴 재사용 · TG · 메모리 · 엔진 로그) + X3 navigate dg 1회(H0, 접두사 cab_<조건>).
# WMI 로 띄운다(launch_cache.ps1). 끝 표시 '[cache] done'. 서버는 내리고 낮 모드는 유지(다음이 H4). 원장 커밋은 Claude 가 대조 뒤.
param([int]$Context = 32768)
$ErrorActionPreference = 'Continue'
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content C:\strata-lab\.secrets\strata-api-key.txt -Raw).Trim()
$eng = 'C:\strata-lab\engine'
"[cache] start $(Get-Date -Format s) commit $(git -C C:\strata-lab rev-parse --short HEAD)"
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\llm-mode.ps1 | Select-Object -Last 1
$conds = @(@{n = 'none'; m = -1}, @{n = 'cm512'; m = 512}, @{n = 'cm1024'; m = 1024})
foreach ($c in $conds) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
  $suffix = if ($c.m -ge 0) { "-cm$($c.m)" } else { '' }
  $elog = Join-Path $eng "strata-qwen36-ctx$Context$suffix.log"
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context $Context -CacheMib $($c.m)" `
    -RedirectStandardOutput "$eng\serve-cache-$($c.n).log" -RedirectStandardError "$eng\serve-cache-$($c.n).err" -WindowStyle Hidden
  $h = $null
  for ($i = 0; $i -lt 120; $i++) {
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
    Start-Sleep -Seconds 5
  }
  "[cache] $($c.n) ready loaded=$($h.loaded) $(Get-Date -Format s)"
  & $py -u C:\strata-lab\scripts\bench\cache_ab.py --cond $c.n --log $elog 2>&1 | ForEach-Object { "[cache] $_" }
  & $py -u C:\strata-lab\scripts\bench\run_x3.py --mode navigate --tasks dg_group_names --prefix "cab_$($c.n)" --harness H0 --tool-out chars --final-turn none --rep-start 1 2>&1 | ForEach-Object { "[cache] $_" }
  "[cache] $($c.n) end $(Get-Date -Format s)"
}
& powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop | Out-Null
"[cache] done $(Get-Date -Format s)"
