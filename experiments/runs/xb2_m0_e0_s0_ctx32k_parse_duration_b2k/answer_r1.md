정규식으로 구조화된 형식을 검증하고, 각 그룹을 추출해 곱셈 후 합산하는 방식으로 구현했습니다. `re.fullmatch`를 사용해 공백 없는 정확한 패턴 매칭과 단위 순서/중복 제한을 한 번에 처리하며, 빈 문자열이나 단위 미포함 시 명시적으로 예외를 발생시킵니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열은 허용되지 않습니다.")
        
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    if not match or all(match.group(i) is None for i in range(1, 5)):
        raise ValueError("유효하지 않은 형식입니다. d, h, m, s 단위 조합만 허용됩니다.")
        
    days = int(match.group(1)[:-1]) if match.group(1) else 0
    hours = int(match.group(2)[:-1]) if match.group(2) else 0
    minutes = int(match.group(3)[:-1]) if match.group(3) else 0
    seconds = int(match.group(4)[:-1]) if match.group(4) else 0
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```