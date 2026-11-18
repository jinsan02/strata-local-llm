# 측정용 전원 설정을 '성능 우선'으로 고정한다. 관리자 PowerShell 에서 사람이 실행한다 (시스템 설정).
#   powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\power-max.ps1
# 전후 값은 env\power-<시각>-before.txt / -after.txt 로 남긴다. 되돌리기: powercfg /restoredefaultschemes
$ErrorActionPreference = 'Stop'
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
  Write-Host '관리자 PowerShell 에서 실행하세요.' -ForegroundColor Red; exit 1 }
$ts = Get-Date -Format 'yyyyMMdd-HHmm'
$envDir = 'C:\strata-lab\env'
$hp = '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'   # 고성능
powercfg /q SCHEME_CURRENT | Out-File "$envDir\power-$ts-before.txt" -Encoding utf8

powercfg /setactive $hp
# 숨겨진 프로세서 항목을 보이게 (값만 바꾸면 되지만 확인하기 쉽게)
powercfg -attributes SUB_PROCESSOR PERFBOOSTMODE -ATTRIB_HIDE
powercfg -attributes SUB_PROCESSOR CPMINCORES -ATTRIB_HIDE

$set = @(
  @('SUB_PROCESSOR','PROCTHROTTLEMIN',100, '최소 프로세서 상태 100%'),
  @('SUB_PROCESSOR','PROCTHROTTLEMAX',100, '최대 프로세서 상태 100%'),
  @('SUB_PROCESSOR','PERFBOOSTMODE',2,     '터보 부스트 적극적'),
  @('SUB_PROCESSOR','CPMINCORES',100,      '코어 파킹 끔 (최소 코어 100%)'),
  @('SUB_PCIEXPRESS','ASPM',0,             'PCIe 링크 절전 끔'),
  @('SUB_DISK','DISKIDLE',0,               '디스크 끄기 안 함'),
  @('SUB_SLEEP','STANDBYIDLE',0,           '절전 안 함'),
  @('SUB_SLEEP','HIBERNATEIDLE',0,         '최대 절전 안 함'),
  @('SUB_SLEEP','HYBRIDSLEEP',0,           '하이브리드 절전 끔'),
  @('SUB_SLEEP','RTCWAKE',0,               '절전 해제 타이머 끔'),
  @('2a737441-1930-4402-8d77-b2bebba308a3','48e6b7a6-50f5-4782-a5d4-53bb8f07e226',0,'USB 선택적 절전 끔')
)
foreach ($s in $set) {
  powercfg /setacvalueindex $hp $s[0] $s[1] $s[2]
  powercfg /setdcvalueindex $hp $s[0] $s[1] $s[2]
  "{0}" -f $s[3]
}
powercfg /setactive $hp
# 최대 절전·빠른 시작 끔 (hiberfil.sys 삭제, 부팅마다 드라이버를 새로 올림)
powercfg /hibernate off
"최대 절전·빠른 시작 끔"
powercfg /q SCHEME_CURRENT | Out-File "$envDir\power-$ts-after.txt" -Encoding utf8
powercfg /getactivescheme
Write-Host "완료. 기록: $envDir\power-$ts-*.txt  (화면 끄기는 성능과 무관해 그대로 둠)" -ForegroundColor Green
