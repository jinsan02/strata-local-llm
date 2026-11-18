**간단한 구현 설명**
- `strip()`로 양옆 공백을 제거하고 빈 문자열은 즉시 예외 처리합니다.
- 정규식 `r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:[0])?(?:\d+s)?$'`를 사용하여 `d, h, m, s`가 **지정된 순서대로 최대 한 번씩** 나타나는지 엄격히 검증합니다.
- `re.fullmatch`로 중간에 공백이나 알 수 없는 문자가 섞인 경우나 단위 누락/중복을 방지합니다.
- 최소한 하나의 단위가 반드시 존재해야 하므로 `any(match.groups())`로 검증 후 각 그룹의 값을 정수로 변환해 초 단위로 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty or whitespace-only string")
        
    match = re.fullmatch(r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:[0])?(?:\d+s)?$', s)
    if not match or not any(match.groups()):
        raise ValueError("Invalid duration format: must contain at least one unit")
        
    days = int(match.group(1) or 0)
    hours = int(match.group(2) or 0)
    minutes = int(match.group(3) or 0)
    seconds = int(match.group(4) or 0)
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```