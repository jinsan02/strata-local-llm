단위 문자열의 형식을 엄격하게 검증하고 순서와 중복을 방지하기 위해 `re` 모듈을 사용합니다. 정규식은 `d, h, m, s` 순서대로 최대 한 번씩 등장하는 패턴을 정의하며, 빈 문자열이나 단위가 누락된 경우를 걸러냅니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
    
    # d -> h -> m -> s 순서, 각 단위 최대 1회 등장, 숫자는 0 이상
    pattern = r'^(\d+d)?(\d+h)?(\d+m)?(\d+s)?$'
    if not re.match(pattern, s):
        raise ValueError("잘못된 형식입니다. (단위 순서, 중복, 알 수 없는 문자 또는 공백)")
    
    conv = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    total = 0
    
    for match in re.finditer(r'(\d+)([dhms])', s):
        num, unit = int(match.group(1)), match.group(2)
        total += num * conv[unit]
        
    # 최소한 하나의 단위가 포함되었는지 명시적 검증 (정규식으로 빈 문자열은 걸렀지만 0일 가능성 대비)
    if total == 0 and not any(c in s for c in "dhms"):
        raise ValueError("유효한 단위 정보가 없습니다.")
        
    return total
```