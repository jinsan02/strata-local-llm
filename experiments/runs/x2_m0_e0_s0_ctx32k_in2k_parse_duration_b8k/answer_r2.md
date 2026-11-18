### 설명
- `strip()`로 앞뒤 공백을 제거합니다.
- `re.fullmatch`에 순서가 고정된 선택적 그룹 `(?:\d+d)?(?:\d+h)?(?:\d+m)?(?:\d+s)?$` 을 사용해 단위 순서, 중복 허용 여부, 공간/알 수 없는 문자 불일치를 한 번에 검증합니다.
- 모든 그룹이 `None`인 경우(빈 문자열이나 단위만 붙은 숫자 외의 순수 숫자 등) `any(groups)` 검사로 걸러내어 `ValueError` 를 발생시킵니다.
- 누락된 단위는 `or 0` 으로 처리해 합산합니다.

### 코드
```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    m = re.fullmatch(r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    
    if not m or not any(m.groups()):
        raise ValueError("Invalid duration format")

    d, h, minute, sec = m.groups()
    return (int(d or 0) * 86400 +
            int(h or 0) * 3600 +
            int(minute or 0) * 60 +
            int(sec or 0))
```