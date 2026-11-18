함수는 `re` 모듈을 사용해 정규식으로 구조를 검증하고 순차적으로 매칭된 숫자를 추출합니다. 단위별 초 환산 계수를 곱해 합산한 후 반환합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    # d, h, m, s 순서만 허용하며 각 단위는 최대 1회 등장
    pattern = r"^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(\d+s)?$"
    match = re.fullmatch(pattern, s)
    
    if not match:
        raise ValueError("형식 또는 순서가 올바르지 않습니다.")
        
    # 최소 한 개 이상의 단위가 포함되어야 함
    if not any(match.groups()):
        raise ValueError("단위가 하나도 지정되지 않았습니다.")
        
    days, hours, minutes, seconds_str = match.groups()
    
    return (int(days or 0) * 86400 +
            int(hours or 0) * 3600 +
            int(minutes or 0) * 60 +
            int(seconds_str.rstrip('s')))
```