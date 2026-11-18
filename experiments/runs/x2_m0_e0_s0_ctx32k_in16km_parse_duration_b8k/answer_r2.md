### 설명
- 정규식 `\s*(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?\s*`로 문자열을 완전히 매칭합니다. 각 단위 블록은 `d → h → m → s` 순서로 고정되고 `?`로 선택적이라 중복이나 순서 위반 시 매칭이 즉시 실패하여 `ValueError`가 발생합니다.
- 양끝의 `\s*`가 앞뒤 공백을 무시하고, 문자열 중간에 공백이나 알 수 없는 문자가 있으면 `fullmatch`가 실패합니다.
- 모든 캡처 그룹이 `None`이면 단위가 하나도 없음을 의미하므로 별도 예외 처리로 걸러냅니다.
- 매칭된 숫자를 정수로 변환해 각 단위별 초 단위(일=86400, 시=3600, 분=60, 초=1)를 곱한 후 합산하여 반환합니다.

```python
import re

def parse_duration(s: str) -> int:
    m = re.fullmatch(r'\s*(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?\s*', s)
    if not m:
        raise ValueError("Invalid duration format")
    
    days, hours, mins, secs = m.groups()
    if all(v is None for v in (days, hours, mins, secs)):
        raise ValueError("Must contain at least one unit (d, h, m, s)")
        
    return int(days or 0) * 86400 + \
           int(hours or 0) * 3600 + \
           int(mins or 0) * 60 + \
           int(secs or 0)
```