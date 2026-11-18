단위와 숫자가 고정된 순서로만 나타나는 패턴이므로, `re.fullmatch`를 사용해 엄격한 형식 검증을 한 번에 수행할 수 있습니다. 공백 제거 후 정규식으로 매칭하고, 최소 하나의 단위가 포함되어야 하며, 존재하는 그룹에서 앞의 단위 문자를 제거해 정수로 변환한 뒤 곱산합산하면 됩니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    # d, h, m, s 순서로 한 번씩만 등장하며 숫자는 필수 (0 이상)
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    
    if not match or not any(match.groups()):
        raise ValueError("올바른 형식이 아닙니다: 단위 없음, 순서 위반, 중복 또는 알 수 없는 문자 포함")
        
    days   = int(match.group(1)[:-1]) if match.group(1) else 0
    hours  = int(match.group(2)[:-1]) if match.group(2) else 0
    minutes = int(match.group(3)[:-1]) if match.group(3) else 0
    seconds = int(match.group(4)[:-1]) if match.group(4) else 0
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```