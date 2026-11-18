앞뒤 공백 제거 후 정규식으로 `d→h→m→s` 순서와 단위 존재 여부를 한 번에 검증합니다. 각 그룹에서 숫자만 추출해 초 단위로 변환한 뒤 합산하고, 조건에 맞지 않으면 `ValueError`를 일으킵니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty string")
        
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    if not match or all(g is None for g in match.groups()):
        raise ValueError("Invalid duration format")
        
    days = int(match.group(1)[:-1]) if match.group(1) else 0
    hours = int(match.group(2)[:-1]) if match.group(2) else 0
    minutes = int(match.group(3)[:-1]) if match.group(3) else 0
    seconds = int(match.group(4)[:-1])
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```