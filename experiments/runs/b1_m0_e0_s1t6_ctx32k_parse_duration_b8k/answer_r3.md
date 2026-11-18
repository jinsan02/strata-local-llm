### 설명
1. `strip()` 로 양쪽 공백을 제거합니다.
2. 정규식 `(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?` 로 전체 문자열이 **d→h→m→s 순서**로 각 단위와 숫자를 최대 한 번씩 포함하는지 검증합니다.
3. `re.fullmatch` 는 내부 공백·알 수 없는 단위·중복/역순·단위 없는 숫자 등을 자동으로 걸러냅니다. 모든 그룹이 `None` 인 경우(빈 문자열 등) `ValueError` 를 발생시킵니다.
4. 매칭된 숫자를 각 단위의 초 환산값(`d:86400, h:3600, m:60, s:1`) 에 곱해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    m = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', s)
    
    if not m or not any(m.groups()):
        raise ValueError("Invalid duration string")
        
    d, h, min_, sec = m.groups()
    return (int(d) if d else 0) * 86400 + \
           (int(h) if h else 0) * 3600 + \
           (int(min_) if min_ else 0) * 60 + \
           int(sec) if sec else 0
```