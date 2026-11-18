정규식을 활용해 입력 구조를 검증하고 단위를 매핑합니다. `strip()`으로 앞뒤 공백을 제거한 후, 패턴이 엄격한 순서(`d→h→m→s`)와 단위 형식만 허용하도록 설계했습니다. 매칭 실패나 빈 문자열은 `ValueError`로 처리하고, 캡처된 숫자를 초 단위로 계산하여 반환합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Invalid duration: empty string")
        
    match = re.fullmatch(r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not match:
        raise ValueError("Invalid duration format")
        
    d = int(match.group(1)) if match.group(1) else 0
    h = int(match.group(2)) if match.group(2) else 0
    m = int(match.group(3)) if match.group(3) else 0
    sec = int(match.group(4)) if match.group(4) else 0
    
    return d * 86400 + h * 3600 + m * 60 + sec
```