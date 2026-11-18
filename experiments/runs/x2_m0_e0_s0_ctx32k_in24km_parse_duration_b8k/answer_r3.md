### 설명
1. `strip()` 로 앞뒤 공백을 제거하고, 빈 문자열이면 즉시 `ValueError` 를 발생시킵니다.
2. `re.fullmatch(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)", s)` 정규식을 적용합니다. 각 단위를 옵션(`?`)으로 순서대로 배치해 **최대 1회 출현**과 **고정된 순서(d→h→m→s)** 를 강제하며, `\d+` 가 반드시 숫자를 요구하므로 단위 없는 숫자나 중간 공백은 매칭되지 않게 됩니다.
3. 매칭에 실패하면 `ValueError`, 성공하면 `groups()` 로 추출한 값을 정수로 변환해 초 단위 합산 후 반환합니다.

### 최종 코드
```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("empty duration string")
        
    match = re.fullmatch(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)", s)
    if not match:
        raise ValueError(f"invalid duration format: {s!r}")
        
    days, hours, minutes, seconds = match.groups()
    return (int(days or 0) * 86400 +
            int(hours or 0) * 3600 +
            int(minutes or 0) * 60 +
            int(seconds or 0))
```