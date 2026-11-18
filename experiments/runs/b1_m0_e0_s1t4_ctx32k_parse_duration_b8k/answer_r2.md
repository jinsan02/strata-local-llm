### 구현 논리
1. `strip()` 로 양끝 공백 제거 후 빈 문자열이면 즉시 `ValueError` 발생.
2. `re.fullmatch`로 전체 문자열을 정확히 매칭합니다. `(?:...)?` 구조로 `d`, `h`, `m`, `s` 순서를 강제하며 각 단위는 최대 1회만 등장하도록 구성했습니다. 이 방식은 공백 포함, 단위 누락 숫자, 순서 위반, 중복, 알 수 없는 문자가 섞인 경우 모두 매칭 실패 (`ValueError`) 로 처리합니다.
3. 정규식에서 추출된 캡처 그룹을 정수로 변환하고, 각 시간 단위의 초 환산 계수(`86400`, `3600`, `60`, `1`)를 곱해 합산 후 반환합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    match = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not match:
        raise ValueError(f"잘못된 형식입니다: {s!r}")
        
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    seconds = int(match.group(4)) if match.group(4) else 0
    
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```