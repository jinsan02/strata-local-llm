### 설명
정규식 `(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?`로 입력 문자열을 정확히 매칭합니다. 각 단위는 순서대로 나타나며 선택적(`?`)으로 처리되어 중간 단위 생략은 허용되지만, 순서가 꼬이거나 (`1m1s`), 중복/모르는 단위 (`1h1x`), 단위 없이 숫자만 있는 경우 (`10`) 는 `fullmatch` 실패로 자동 필터링됩니다. 최종적으로 하나 이상의 단위가 반드시 존재해야 하므로 `all(g is None)` 검사로 빈 문자열이나 단위 누락 시 `ValueError`를 일으킵니다.

### 코드
```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    # d, h, m, s 순서대로 각 단위가 최대 한 번 등장 (선택적)
    m = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', s)
    if not m or all(g is None for g in m.groups()):
        raise ValueError(f"Invalid duration string: {s!r}")
        
    days, hours, minutes, seconds = m.groups()
    return (int(days or 0) * 86400 + 
            int(hours or 0) * 3600 + 
            int(minutes or 0) * 60 + 
            int(seconds or 0))
```