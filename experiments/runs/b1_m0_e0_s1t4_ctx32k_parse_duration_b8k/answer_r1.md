단순 정규식으로 `d, h, m, s` 순서와 각 단위당 숫자 존재를 엄격히 검증한 후, 일치하는 그룹만 추출하여 초 단위로 계산합니다. 공백은 입력 전 제거하며, 매칭 실패 또는 비어있는 문자열은 명시적으로 `ValueError`로 처리합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
    
    # d, h, m, s 순서만 허용하며 각 단위는 1회만 등장 가능
    match = re.fullmatch(r'^(\d+d)?(\d+h)?(\d+m)?(\d+s)?$', s)
    if not match:
        raise ValueError(f"잘못된 기간 형식입니다: '{s}'")
        
    # 그룹에서 단위 문자 제거 후 정수로 변환 (없으면 0)
    def to_sec(grp: str | None) -> int:
        return int(grp[:-1]) if grp else 0
        
    return to_sec(match.group(1)) * 86400 + \
           to_sec(match.group(2)) * 3600 + \
           to_sec(match.group(3)) * 60 + \
           to_sec(match.group(4)) * 1
```