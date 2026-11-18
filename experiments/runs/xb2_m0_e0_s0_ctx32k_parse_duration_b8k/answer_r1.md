정규식 `re.fullmatch`를 사용해 입력의 모든 검증 규칙(순서, 중복 없음, 단위 필수, 내부 공백 금지 등)을 한 번에 검사합니다. 매칭된 그룹을 추출한 후 각 단위를 초 단위로 변환해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    # d, h, m, s 순서대로 0개 또는 1번씩 등장하는지 일괄 검증
    match = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', s)
    if not match:
        raise ValueError("잘못된 기간 형식입니다.")
        
    d, h, m, sec = match.groups()
    return (int(d or 0) * 86400 + 
            int(h or 0) * 3600 + 
            int(m or 0) * 60 + 
            int(sec or 0))
```