입력 문자열의 형식, 단위 순서, 중복 여부를 한 번에 검증하기 위해 고정 그룹 순서의 정규식을 사용합니다. `(\d+d)?(\d+h)?(\d+m)?(\d+s)` 패턴은 단위的出现 순서(d→h→m→s)와 각 단위의 등장 횟수(0~1회)를 자동으로 보장하며, 마지막 `(d+s)`가 필수이므로 단위 없는 숫자나 빈 문자열은 매칭되지 않아 `ValueError`로 처리됩니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
    
    # 단위 순서(d→h→m→s) 강제, 각 단위 등장 횟수 0~1회 자동 보장, 마지막 단위(s) 필수
    m = re.fullmatch(r"(\d+d)?(\d+h)?(\d+m)?(\d+s)", s)
    if not m:
        raise ValueError(f"잘못된 기간 형식입니다: '{s}'")
        
    days, hours, minutes, seconds = m.groups()
    return (int(days or 0) * 86400 + 
            int(hours or 0) * 3600 + 
            int(minutes or 0) * 60 + 
            int(seconds or 0))
```