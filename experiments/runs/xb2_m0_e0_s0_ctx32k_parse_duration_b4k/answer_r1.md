`strip()`로 앞뒤 공백을 제거한 후, `re.fullmatch`를 사용해 `(d)?(h)?(m)?(s)?` 순서로 단위가 최대 한 번씩만 등장하는지 엄격히 검증합니다. 패턴 불일치(`ValueError`) 및 단위 미포함(숫자만 입력) 체크 후, 그룹별로 매칭된 수치를 초 단위 변환 계수(d:86400, h:3600, m:60, s:1)에 곱해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    # d → h → m → s 순서, 각 단위 최대 1회 등장, 숫자 필수
    pattern = r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)$'
    match = re.fullmatch(pattern, s)
    
    if not match or all(g is None for g in match.groups()):
        raise ValueError("유효하지 않은 형식입니다.")
        
    d, h, m, sec = match.groups()
    return (int(d) * 86400 if d else 0) + \
           (int(h) * 3600 if h else 0) + \
           (int(m) * 60 if m else 0) + \
           (int(sec) if sec else 0)
```