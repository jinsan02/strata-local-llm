정규식으로 `d→h→m→s` 순서와 각 단위 최대 1회를 엄격하게 검열합니다. `strip()`으로 양 끝 공백만 제거해 내부 공백·빈 문자열·단위 없는 숫자·알 수 없는 문자를 즉시 실패 처리하며, 일치한 그룹에서 접미사를 분리해 시간 가중치(86400, 3600, 60, 1)를 곱해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
        
    match = re.fullmatch(r'^(\d+d)?(\d+h)?(\d+m)?(\d+s)?$', s.strip())
    if not match or not any(match.groups()):
        raise ValueError(f"Invalid duration format: {s!r}")
        
    days, hours, minutes, secs = match.groups()
    return (int(days[:-1]) * 86400 if days else 0) + \
           (int(hours[:-1]) * 3600 if hours else 0) + \
           (int(minutes[:-1]) * 60 if minutes else 0) + \
           (int(secs[:-1]) if secs else 0)
```