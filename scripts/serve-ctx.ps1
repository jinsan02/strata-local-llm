# 같은 모델·엔진·설정에서 --max-context 만 바꾼 서버 설정을 만들고 서버를 띄운다 (X0·X1).
# setup.py 가 만든 strata-qwen36-ud-q4_k_xl.json 을 원본으로 두고, 사본 strata-qwen36-ctx<N>.json 을 쓴다.
# -Stop 만 주면 떠 있는 서버를 내린다.
param(
  [int]$Context = 16384,
  [string]$Host_ = '127.0.0.1',     # X4 에서만 Tailscale 주소
  [switch]$Stop
)
$ErrorActionPreference = 'Continue'
$eng = 'C:\strata-lab\engine'
function Stop-Strata {
  Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'serve\\server\.py' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; "[serve] stopped server.py pid $($_.ProcessId)" }
  Get-Process strata -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.Id -Force; "[serve] stopped strata.exe pid $($_.Id)" }
  Start-Sleep -Seconds 3
}
Stop-Strata
if ($Stop) { return }

$src = Join-Path $eng 'strata-qwen36-ud-q4_k_xl.json'
$dst = Join-Path $eng "strata-qwen36-ctx$Context.json"
$cfg = Get-Content $src -Raw | ConvertFrom-Json
foreach ($key in 'args','args_written') {
  $a = [System.Collections.ArrayList]@($cfg.$key)
  $i = $a.IndexOf('--max-context'); $a[$i + 1] = "$Context"
  $cfg.$key = @($a)
}
$cfg.log = Join-Path $eng "strata-qwen36-ctx$Context.log"
[IO.File]::WriteAllText($dst, ($cfg | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding($false)))
"[serve] config $dst  (--max-context $Context, host $Host_)"
$env:PYTHONUTF8 = '1'
Set-Location $eng
& C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe serve\server.py --engine strata --config $dst --port 8080 --host $Host_ 2>&1
