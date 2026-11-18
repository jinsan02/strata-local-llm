규칙에 따라 순서와 중복을 엄격히 제한하고, 숫자/단위 매칭 및 공백 처리를 정규식으로 한 번에 검증합니다. 빈 문자열이나 단위 없는 입력은 `any(m.groups())` 체크로 걸러내며, 결측 그룹은 기본값 0으로 처리해 합산합니다.

```python
import re

_DURATION_RE = re.compile(r"\s*(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(\d+s)\s*")

def parse_duration(s: str) -> int:
    m = _DURATION_RE.fullmatch(s)
    if not m or not any(m.groups()):
        raise ValueError("Invalid duration string")
    
    days, hours, minutes, seconds = m.groups()
    return (int(days or 0) * 86400 +
            int(hours or 0) * 3600 +
            int(minutes or 0) * 60 +
            int(seconds))
```