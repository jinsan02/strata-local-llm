### 설명
정규식 `^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$`을 사용해 `d, h, m, s` 순서대로 각 단위가 **최대 한 번씩** 등장하고 그 외의 문자(내부 공백, 알 수 없는 단위 등)가 없음을 검증합니다. `strip()`으로 양 끝 공백만 제거하고, 일치하는 그룹이 하나도 없으면 `"단위 없는 숫자"` 또는 `"빈 문자열"` 예외로 처리합니다. 이후 추출된 수치를 각 단위별 초 단위로 환산해 합산하면 됩니다.

### 최종 코드
```python
import re

def parse_duration(s: str) -> int:
    """기간 문자열을 초 단위 정수로 변환합니다."""
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열은 허용되지 않습니다.")
        
    # d, h, m, s 순서대로 최대 한 번씩 등장하며 내부는 공백이 없어야 합니다.
    m = re.fullmatch(r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not m or not any(m.groups()):
        raise ValueError("잘못된 형식입니다. 단위(d, h, m, s)를 지정하고 순서와 중복 규칙을 지켜야 합니다.")
        
    days = int(m.group(1)) if m.group(1) else 0
    hours = int(m.group(2)) if m.group(2) else 0
    minutes = int(m.group(3)) if m.group(3) else 0
    seconds = int(m.group(4)) if m.group(4) else 0
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```