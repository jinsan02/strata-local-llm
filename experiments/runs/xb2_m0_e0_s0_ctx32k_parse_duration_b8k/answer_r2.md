`strip()`로 양쪽 공백을 제거하고 빈 문자열 여부를 체크합니다. 이후 정규식 `^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$` 로 입력 형식을 엄격히 검증합니다. 이 패턴은 단위 순서(d→h→m→s), 중복 방지, 미포함 허용을 한 번에 처리하며, 숫자나 알 수 없는 단위, 내부 공백 등은 매칭 실패로 `ValueError` 가 유발됩니다. 검증된 그룹의 숫자를 추출해 각 단위의 초 변환 계수(`86400, 3600, 60, 1`)에 곱해 합산하면 됩니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    match = re.fullmatch(r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not match:
        raise ValueError("지원하지 않는 형식입니다.")
        
    d = int(match.group(1) or "0")
    h = int(match.group(2) or "0")
    min_val = int(match.group(3) or "0")
    sec = int(match.group(4) or "0")
    
    return d * 86400 + h * 3600 + min_val * 60 + sec
```