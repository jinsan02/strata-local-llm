### 접근 방식
1. `strip()`로 앞뒤 공백을 제거한 후, `re.fullmatch`로 전체 문자열과 매칭합니다.
2. 정규식 `(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?`는 `d → h → m → s` 순서만 허용하며, 각 단위 그룹이 선택사항(`?`)으로 되어 있어 중간 단위 생략을 자연스럽게 지원합니다. 이 구조상 중복·비순서 입력은 매칭 실패로 처리됩니다.
3. 모든 캡처 그룹이 `None`인 경우(빈 문자열 또는 단위 누락)와 정규식 실패 시 `ValueError`를 발생시킵니다.
4. 매칭된 숫자를 정수로 변환해 각 단위별 초 단위 곱셈 후 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    match = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', s)
    if not match or not any(match.groups()):
        raise ValueError(f"Invalid duration format: {s!r}")

    days, hours, minutes, seconds = (int(g or '0') for g in match.groups())
    return days * 86400 + hours * 3600 + minutes * 60 + seconds
```