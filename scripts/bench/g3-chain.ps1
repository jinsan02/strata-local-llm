# 11-21 Q1-0c 적재 점검 + G3 (사용자: 현재 수준으로 push 하고 다음 진행). docs/q1-plan-20261120.md 5 · 6절.
#   0c : 후보마다 32K 기동 성공 · 슬롯 수 · 긴 입력 PP(약 1.6만 토큰, max_tokens 1, 서로 다른 앞머리로 2회). M0 도 같은 PP 측정만 한다.
#        N0(MTP 제거)는 Q17 이 greedy 30회 후보로 남아 보류(MTP 가 다시 필요할 수 있음).
#   G3 : H0 + card-coding, 6과제 x 2회(seed 42 · 43), 접두사 x3g3. 대조 = x3s1c 1 · 2회차(7/12, 다시 안 돌림). 탈락 = 대조보다 3 넘게 나쁨(< 4/12).
# 순서: M0 PP → M1b(PP · X3) → M1a(PP · X3). 모델마다 서버는 한 번만 띄운다. 끝나면 서버 종료 · 밤 모드. 끝 표시 '[g3] done'.
param([int]$Context = 32768, [int]$Reps = 2, [string[]]$Only = @(), [int]$RepStart = 1,   # 11-21 G4: -RepStart 3 -Reps 5 = G3 의 1 · 2회차에 3~5회차를 더해 30회(두 번 안 돌림)
      [string]$Harness = 'H0', [string]$Prefix = 'x3g3', [ValidateSet('strict', 'lenient')][string]$EditApply = 'strict', [switch]$ForceX3, [switch]$Mask)   # 11-21 H7: -Only M0 -ForceX3 -Harness H7 -Prefix x3h7 -EditApply lenient -Reps 5
$ErrorActionPreference = 'Continue'
$R = 'C:\strata-lab'; $D = "$R\data\models"
$py = 'C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe'
$env:PYTHONUTF8 = '1'
$env:STRATA_API_KEY = (Get-Content "$R\.secrets\strata-api-key.txt" -Raw).Trim()
$hdr = @{ Authorization = "Bearer $env:STRATA_API_KEY" }
$models = [ordered]@{
  M0  = @{ path = "$D\qwen36-ud-q4_k_xl\Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf"; sha = '55983c5a'; x3 = $false }
  M1b = @{ path = "$D\qwen36-m1b\Qwen3.6-35B-A3B-M1B.gguf"; sha = 'cb2eaf34'; x3 = $true }
  M1a = @{ path = "$D\qwen36-m1a\Qwen3.6-35B-A3B-M1A.gguf"; sha = '7d4c5c2f'; x3 = $true }
  M1e = @{ path = "$D\qwen36-m1e\Qwen3.6-35B-A3B-M1E.gguf"; sha = '5b4f868d'; x3 = $true }   # 11-21: down IQ4_NL
  M2 = @{ path = "$D\qwen36-m2\Qwen3.6-35B-A3B-M2.gguf"; sha = ''; x3 = $true }   # 11-21: gate/up IQ4_XS, down M0 그대로 (sha 는 생성 뒤 G0 줄)
}
function Start-Model([string]$id, [string]$path) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\serve-ctx.ps1" -Stop | Out-Null
  $tag = "g3-$($id.ToLower())"
  $log = "$R\engine\strata-qwen36-ctx$Context-$tag.log"
  if (Test-Path $log) { Remove-Item $log }
  $margs = if ($id -eq 'M0') { '' } else { " -Model `"$path`"" }
  $t0 = Get-Date
  Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File $R\scripts\serve-ctx.ps1 -Context $Context -Tag $tag$margs" `
    -RedirectStandardOutput "$R\engine\serve-$tag.log" -RedirectStandardError "$R\engine\serve-$tag.err" -WindowStyle Hidden
  $h = $null
  for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 5
    try { $h = Invoke-RestMethod http://127.0.0.1:8080/health -TimeoutSec 3; if ($h.max_context -eq $Context -and $h.loaded) { break } } catch {}
  }
  $s = -1
  if (Test-Path $log) { $m = Select-String -Path $log -Pattern 'hybrid experts: (\d+) of 256' | Select-Object -Last 1; if ($m) { $s = [int]$m.Matches[0].Groups[1].Value } }
  $vram = (& nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits) -join ''
  $ram = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)
  "[g3] $id loaded=$([bool]($h -and $h.loaded)) load_s=$([int]((Get-Date) - $t0).TotalSeconds) slots=$s vram_mib=$vram free_ram_gb=$ram"
  if (-not ($h -and $h.loaded)) {
    "[g3] 오류: $id 적재 실패 - 엔진 로그 끝:"
    if (Test-Path $log) { Get-Content $log -Tail 15 | ForEach-Object { "[g3]   $_" } }
    Get-Content "$R\engine\serve-$tag.log", "$R\engine\serve-$tag.err" -Tail 10 -ErrorAction SilentlyContinue | ForEach-Object { "[g3]   $_" }
    return $false
  }
  return $true
}
function Probe-PP([string]$id) {
  $txt = (Get-Content "$R\docs\q1-plan-20261120.md" -Raw -Encoding utf8) + (Get-Content "$R\scripts\bench\run_x3.py" -Raw -Encoding utf8)
  while ($txt.Length -lt 48000) { $txt += $txt }
  $txt = $txt.Substring(0, 48000)
  foreach ($k in 1, 2) {
    $body = @{ model = 'strata'; stream = $false; max_tokens = 1; temperature = 0; messages = @(@{ role = 'user'; content = "[probe $id $k $(Get-Random)]`n$txt`n요약 한 단어." }) } | ConvertTo-Json -Depth 5
    $sw = [Diagnostics.Stopwatch]::StartNew()
    try {
      $r = Invoke-RestMethod http://127.0.0.1:8080/v1/chat/completions -Method Post -Headers $hdr -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 900
      $sw.Stop(); $pt = $r.usage.prompt_tokens
      "[g3] $id PP probe $k prompt_tokens=$pt ms=$($sw.ElapsedMilliseconds) pp_tps=$([math]::Round($pt / ($sw.ElapsedMilliseconds / 1000), 1))"
    } catch { "[g3] 경고: $id PP probe $k 실패 $($_.Exception.Message)" }
  }
}
"[g3] start $(Get-Date -Format s) commit $(git -C $R rev-parse --short HEAD)"
if (Get-Process llama-quantize, llama-imatrix, llama-perplexity -ErrorAction SilentlyContinue) { "[g3] 다른 llama 작업이 떠 있음 - 중단"; "[g3] done $(Get-Date -Format s)"; exit 1 }
$gpu = Start-Process nvidia-smi -ArgumentList "--query-gpu=timestamp,temperature.gpu,clocks.sm,clocks.mem,power.draw,memory.used,clocks_event_reasons.active --format=csv -l 60 -f $R\engine\gpu-g3.csv" -WindowStyle Hidden -PassThru
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\llm-mode.ps1" | Select-Object -Last 1
$tasks = @('dg_group_names', 'marker_extras', 'version_bump', 'tags_platform_filter', 'metadata_extra_dupes', 'specifier_bounds')
$hb = @('--harness', $Harness, '--tool-out', 'chars', '--reasoning-echo', 'none', '--final-turn', 'none', '--seed-per-rep', '--sampling', 'card-coding', '--edit-apply', $EditApply, '--ctx', $Context)   # 11-21 25-4: --ctx 를 넘김(전에는 run_x3 기본 32768)
if ($Mask) { $hb += @('--mask', 'on') }   # 11-21 25-4 L2
"[g3] harness $Harness prefix $Prefix edit-apply $EditApply ctx $Context mask $([bool]$Mask)"
foreach ($id in $models.Keys) {
  if ($Only.Count -and $id -notin $Only) { continue }
  $m = $models[$id]
  if (-not (Test-Path $m.path)) { "[g3] 오류: $id 파일 없음 $($m.path)"; continue }
  "[g3] $id hash $(Get-Date -Format s)"
  $sha = (Get-FileHash $m.path -Algorithm SHA256).Hash.ToLower()
  if ($m.sha -and -not $sha.StartsWith($m.sha)) { "[g3] 오류: $id sha256 $sha 이 기록($($m.sha)…)과 다름 - 건너뜀"; continue }
  "[g3] $id sha256 $sha"
  # Start-Model 의 글줄과 성공 여부가 한 배열로 돌아온다: 글줄은 찍고, 마지막 값(bool)으로 판정
  $out = @(Start-Model $id $m.path)
  $out | Where-Object { $_ -is [string] }
  if (-not $out[-1]) { continue }
  Probe-PP $id
  if (-not $m.x3 -and -not $ForceX3) { continue }
  # 주의: PowerShell 변수 이름은 대소문자를 가리지 않는다 - 회차 변수를 $r 로 쓰면 $R(저장소 경로)을 덮는다 (11-21 첫 실행 버그)
  for ($rep = $RepStart; $rep -le $Reps; $rep++) {
    "[g3] $id rep $rep $(Get-Date -Format s)"
    & $py -u "$R\scripts\bench\run_x3.py" --mode navigate --tasks @tasks --prefix $Prefix @hb --rep-start $rep --model-id $id --model-sha256 $sha 2>&1 | ForEach-Object { "[g3] $_" }
    "[g3] $id rep $rep end $(Get-Date -Format s)"
  }
}
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\serve-ctx.ps1" -Stop | Out-Null
if ($gpu -and -not $gpu.HasExited) { Stop-Process -Id $gpu.Id -Force }
& powershell -NoProfile -ExecutionPolicy Bypass -File "$R\scripts\user-mode.ps1" | Select-Object -Last 1 | ForEach-Object { "[g3] $_" }
"[g3] done $(Get-Date -Format s)"
