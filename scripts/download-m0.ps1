# M0 모델 파일을 고정 리비전에서 받고 게시된 sha256 과 대조한다 (이어받기 가능).
param(
  [string]$Repo = 'unsloth/Qwen3.6-35B-A3B-MTP-GGUF',
  [string]$Revision = '5bc3e238d916f48a861bac2f8a1990a0e9b7e98d',
  [string]$File = 'Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf',
  [string]$Sha256 = '55983c5a75a1ab969824077b3bb3de4146e82a9234072b48ad4e8f92ad3fe9f1',
  [string]$Dest = 'C:\strata-lab\data\models\qwen36-ud-q4_k_xl'
)
$ErrorActionPreference = 'Continue'
New-Item -ItemType Directory -Force $Dest | Out-Null
$out = Join-Path $Dest $File
$url = "https://huggingface.co/$Repo/resolve/$Revision/$File"
"[m0] $url -> $out  $(Get-Date -Format s)"
$t0 = Get-Date
curl.exe -sSL --fail --retry 5 --retry-delay 10 -C - -o $out $url
"[m0] curl exit $LASTEXITCODE  $([math]::Round(((Get-Date)-$t0).TotalMinutes,1)) min"
$got = (Get-FileHash $out -Algorithm SHA256).Hash.ToLower()
"[m0] size $((Get-Item $out).Length) bytes"
"[m0] sha256 $got"
if ($got -eq $Sha256) { "[m0] hash OK (revision $Revision)" } else { "[m0] HASH MISMATCH, expected $Sha256" }
"[m0] done $(Get-Date -Format s)"
