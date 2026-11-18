앞뒤 공백은 `strip()`으로 제거하고, 정규식 `^(\d+d)?(\d+h)?(\d+m)?(\d+s)?$`으로 **형식·순서·중복 여부**를 단일 매칭으로 검증합니다. 매칭 실패 또는 실제 단위가 하나도 포함되지 않으면 `ValueError`를 발생시키고, 성공 시 포착된 숫자-단위 쌍을 미리 정의한 계수표와 곱해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    if not match or not any(match.groups()):
        raise ValueError("Invalid duration format")
        
    multipliers = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    return sum(
        int(val[:-1]) * multipliers[unit]
        for val, unit in zip(match.groups(), "dhms")
        if val
    )
```