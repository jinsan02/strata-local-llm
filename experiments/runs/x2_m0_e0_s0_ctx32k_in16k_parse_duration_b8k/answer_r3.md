### 설계 및 규칙 설명
1. **공백 처리**: 입력 문자열의 앞뒤 공백만 제거하고, 내부 공백은 정규식이 매칭되지 않도록 하여 `ValueError`를 유발합니다.
2. **형식 검증**: `re.fullmatch`로 전체 문자열을 엄격하게 검사합니다. 패턴 `(\d+d)?(\d+h)?(\d+m)?(\d+s)?`는 지정된 순서(d→h→m→s)대로 단위가 등장하며, 각 단위는 최대 한 번만 나타나고 누락도 허용되도록 구성했습니다.
3. **유효성 확인**: 정규식 매칭 실패 또는 모든 그룹이 `None`인 경우(단위 하나도 없는 경우) `ValueError`를 발생합니다.
4. **계산**: 매칭된 그룹에서 숫자 부분만 추출해 누락 단위는 `0`으로 간주하고, 시간 단위를 초로 환산하여 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열이거나 공백만 포함할 수 없습니다.")
    
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    if not match or not any(match.groups()):
        raise ValueError("지원하는 형식이 아닙니다. 최소 한 개의 단위(d, h, m, s)가 필요합니다.")
        
    days = int(match.group(1) or 0)
    hours = int(match.group(2) or 0)
    minutes = int(match.group(3) or 0)
    seconds = int(match.group(4) or 0)
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```