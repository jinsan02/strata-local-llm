규칙을 정규식으로 명확히 분리하여 검증하고 계산합니다. `strip()`로 양끝 공백을 제거한 후, `re.fullmatch`로 `(d→h→m→s)` 순서와 단위 존재 여부(최대 1회)를 한 번에 검사합니다. 위반 시 바로 `ValueError`를 던지며, 매칭된 그룹에서 숫자 부분만 추출해 초 단위 계수를 곱해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty duration string")

    # d→h→m→s 순서 strict 적용, 각 단위는 최대 1회 등장 (없는 경우 Optional)
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    if not match:
        raise ValueError(f"Invalid duration format: {s!r}")

    total = 0
    days, hours, minutes, seconds = match.groups()
    if days:   total += int(days[:-1]) * 86_400
    if hours:  total += int(hours[:-1]) * 3_600
    if minutes: total += int(minutes[:-1]) * 60
    if seconds: total += int(seconds[:-1])

    return total
```