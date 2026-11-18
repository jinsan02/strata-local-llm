### 설명
1. 양쪽 공백은 `.strip()`으로 제거하고, 빈 문자열이면 즉시 `ValueError` 발생.
2. 정규식 `fullmatch`로 `(숫자+단위)` 패턴을 순서(`d→h→m→s`)와 단일 존재 조건에 맞게 검증. 순서 위반, 중복, 알 수 없는 문자/공백/단위 없는 숫자는 매칭 실패로 `ValueError` 처리.
3. 매칭된 각 그룹의 숫자를 정수로 변환해 `(days*86400 + hours*3600 + minutes*60 + seconds)`를 반환.

### 코드
```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty duration string")
        
    match = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', s)
    if not match:
        raise ValueError(f"Invalid duration format: '{s}'")
        
    days, hours, minutes, seconds = (int(g) if g else 0 for g in match.groups())
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```