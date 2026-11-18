정규식 구조를 이용해 단위 순서와 중복 여부를 한 번에 검증합니다. `strip()`으로 양쪽 공백만 제거하고, 내부 공백이나 단위 누락/순서 위반 등은 정규식이 실패하도록 설계해 자연스럽게 `ValueError`를 발생시킵니다. 추출한 숫자를 각 단위의 초 환산 계수(일:86400, 시:3600, 분:60, 초:1)에 곱해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    m = re.fullmatch(r'((\d+)d)?((\d+)h)?((\d+)m)?((\d+)s)?', s)
    if not m:
        raise ValueError(f"잘못된 기간 형식: {s!r}")
        
    days = int(m.group(2)) if m.group(2) else 0
    hours = int(m.group(4)) if m.group(4) else 0
    minutes = int(m.group(6)) if m.group(6) else 0
    seconds = int(m.group(8)) if m.group(8) else 0
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```