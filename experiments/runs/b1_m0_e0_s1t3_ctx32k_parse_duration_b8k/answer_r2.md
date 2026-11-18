단위와 숫자를 고정된 순서로 매칭하는 정규식으로 처리하면 조건을 간결하게 만족할 수 있습니다. `re.fullmatch`를 사용해 문자열 전체가 패턴과 정확히 일치하는지 검증하고, 누락된 단위는 `0`으로 취급합니다. 앞뒤 공백은 `strip()`으로 제거하며, 공백 내포나 형식 오류는 정규식 실패로 자연스럽게 `ValueError`를 발생시킵니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty or whitespace-only string")
    
    match = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not match:
        raise ValueError("Invalid format, order, or contains unsupported characters/whitespace")
        
    days = int(match.group(1) or 0)
    hours = int(match.group(2) or 0)
    minutes = int(match.group(3) or 0)
    seconds = int(match.group(4) or 0)
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```