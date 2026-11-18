단위별 변환 상수를 사전에 정의하고, 정규식으로 `d`, `h`, `m`, `s` 순서와 중복/생략 규칙을 한 번에 검증합니다. 앞뒤 공백은 `strip()`으로 제거하고, 매칭 실패 시 명시적으로 `ValueError`를 발생시킵니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
    
    # d, h, m, s 순서대로 각 단위 1회 출현만 허용
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    if not match:
        raise ValueError("잘못된 형식입니다.")
        
    total = 0
    for g in match.groups():
        num, unit = int(g[:-1]), g[-1]
        total += {'d': 86400, 'h': 3600, 'm': 60, 's': 1}[unit] * num
        
    return total
```