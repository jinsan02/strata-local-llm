### 구현 요약
1. 입력의 앞뒤 공백을 `.strip()`으로 제거하고, 빈 문자열일 경우 즉시 `ValueError` 발생.
2. 정규식 `(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?`를 사용해 **순서 고정**, **단위 중복 금지**, **숫자+단위 결합** 형식을 한 번에 검증.
3. 정규식 매칭 실패 또는 모든 단위가 누락된 경우 `ValueError` 발생.
4. 캡처된 그룹을 정수로 변환해 일(`86400`), 시(`3600`), 분(`60`), 초(`1`) 계수를 곱한 값을 합산하여 반환.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열이거나 공백만 포함됩니다.")

    # 순서(d, h, m, s), 중복 금지, 단위 필수 형식 검증
    match = re.fullmatch(r'(?:([0-9]+)d)?(?:([0-9]+)h)?(?:([0-9]+)m)?(?:([0-9]+)s)?', s)
    if not match:
        raise ValueError("지원되지 않는 형식입니다.")

    d, h, m, sec = match.groups()
    if all(v is None for v in (d, h, m, sec)):
        raise ValueError("최소 하나의 시간 단위가 필요합니다.")

    return int(d or 0) * 86400 + int(h or 0) * 3600 + int(m or 0) * 60 + int(sec or 0)
```