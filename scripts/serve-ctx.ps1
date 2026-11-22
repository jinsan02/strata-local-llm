# 같은 모델·엔진·설정에서 --max-context 만 바꾼 서버 설정을 만들고 서버를 띄운다 (X0·X1).
# setup.py 가 만든 strata-qwen36-ud-q4_k_xl.json 을 원본으로 두고, 사본 strata-qwen36-ctx<N>.json 을 쓴다.
# -Stop 만 주면 떠 있는 서버를 내린다.
param(
  [int]$Context = 16384,
  [string]$Host_ = '127.0.0.1',     # X4 에서만 Tailscale 주소
  [int]$CacheMib = -1,              # 0 이상이면 --conversation-cache-mib N (T-013). -1 = 엔진 자동(남은 RAM 4GiB 미만이면 꺼짐)
  [string]$ExtraArgs = '',          # 엔진 인자 덧붙임 (P-diag, 예: '--expert-slots 40'). 공백으로 나눈다
  [string]$EnvSet = '',             # 서버 · 엔진 환경 변수 'K=V;K2=V2' (예: STRATA_Q36_NO_MMQ=1)
  [string]$Tag = '',                # 엔진 로그 이름 꼬리 (ctx<N>-<tag>.log)
  [string]$Model = '',              # 11-21 Q1: 모델 GGUF 경로 바꾸기 (빈 값 = 원본 M0). 러너는 --model-id 로 파일 이름을 확인한다
  [string]$Exe = '',                # 11-22 E1: 엔진 실행 파일 바꾸기 (빈 값 = E0 engine\engine\strata.exe). 턴 체크포인트는 -EnvSet STRATA_Q36_TURN_CKPT=1
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
# 루프백이 아닌 주소(X4 의 Tailscale)로 열 때는 키 없이 열지 않는다 (2026-11-19 토의 7번). 떠 있는 서버를 내리기 전에 검사한다.
# 서버는 $env:STRATA_API_KEY 를 키로 쓴다. 비었거나 'none' · 러너 기본값 'strata-local' · 16자 미만이면 거부.
if (-not $Stop -and $Host_ -notin @('127.0.0.1', 'localhost', '::1')) {
  $k = "$env:STRATA_API_KEY"
  if (-not $k.Trim() -or $k -eq 'none' -or $k -eq 'strata-local' -or $k.Length -lt 16) {
    "[serve] 거부: $Host_ 로 열려면 STRATA_API_KEY 에 16자 이상의 실제 키가 필요하다 (지금: $(if ($k) { '부적합' } else { '없음' }))"
    exit 2
  }
}
Stop-Strata
if ($Stop) { return }

$src = Join-Path $eng 'strata-qwen36-ud-q4_k_xl.json'
$dst = Join-Path $eng "strata-qwen36-ctx$Context.json"
$cfg = Get-Content $src -Raw | ConvertFrom-Json
if ($Exe) {
  if (-not (Test-Path $Exe)) { "[serve] 거부: 실행 파일 없음 $Exe"; exit 2 }
  $cfg.exe = $Exe
}
# 11-19 설정 고정: 출력에 영향을 주는 서버 기본값을 config 에 그대로 적는다(행동 불변, 엔진 버전이 바뀌어도 같은 값)
$pin = [ordered]@{answer_room = $true; repeat_stop_tokens = 256; tool_call_recovery = $true; undeclared_tool_calls = 'text';
  fit_max_tokens = $true; reasoning_loop_recovery = $false; reasoning_close_retry = $false}
foreach ($k in $pin.Keys) { $cfg | Add-Member -NotePropertyName $k -NotePropertyValue $pin[$k] -Force }
foreach ($key in 'args','args_written') {
  $a = [System.Collections.ArrayList]@($cfg.$key)
  $i = $a.IndexOf('--max-context'); $a[$i + 1] = "$Context"
  if ($Model) {
    if (-not (Test-Path $Model)) { "[serve] 거부: 모델 파일 없음 $Model"; exit 2 }
    $j = $a.IndexOf('--native'); $a[$j + 1] = $Model
  }
  if ($CacheMib -ge 0) { [void]$a.Add('--conversation-cache-mib'); [void]$a.Add("$CacheMib") }
  foreach ($x in ($ExtraArgs -split '\s+' | Where-Object { $_ })) { [void]$a.Add($x) }
  $cfg.$key = @($a)
}
$cfg.log = Join-Path $eng ("strata-qwen36-ctx$Context" + $(if ($CacheMib -ge 0) { "-cm$CacheMib" } else { '' }) + $(if ($Tag) { "-$Tag" } else { '' }) + '.log')
[IO.File]::WriteAllText($dst, ($cfg | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding($false)))
"[serve] config $dst  (--max-context $Context, host $Host_, conversation-cache-mib $(if ($CacheMib -ge 0) { $CacheMib } else { 'auto' }), exe $($cfg.exe))"
$env:PYTHONUTF8 = '1'
# 11-19 설정 고정: 웹 UI 의 Chat 공유 설정이 모든 요청 기본값을 바꾸지 않게 한다
$shared = Join-Path $eng ("strata-qwen36-ctx$Context" + '.shared-settings.json')
if (Test-Path $shared) { $bak = "$shared.bak-$(Get-Date -Format yyyyMMddHHmmss)"; Move-Item $shared $bak; "[serve] 경고: Chat 공유 설정 파일을 옮김 -> $bak" }
Get-ChildItem env: | Where-Object { $_.Name -like 'STRATA_*' -and $_.Name -ne 'STRATA_API_KEY' } |
  ForEach-Object { Remove-Item "env:$($_.Name)"; "[serve] 경고: 예상 밖 환경 변수 $($_.Name) 를 지움" }
foreach ($kv in ($EnvSet -split ';' | Where-Object { $_ })) { $k, $v = $kv -split '=', 2; Set-Item "env:$k" $v; "[serve] env $k=$v" }
Set-Location $eng
& C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe serve\server.py --engine strata --config $dst --port 8080 --host $Host_ 2>&1
