정규식(`\s*(?:(\d+)d)?...`)로 전체 문자열을 매칭해 앞뒤 공백만 허용하고, `d→h→m→s` 순서와 각 단위 1회 출현을 구조적으로 강제합니다. 매칭이 실패하거나 시간 단위가 하나도 추출되지 않으면 `ValueError`를 발생시키고, capture된 숫자를 각각의 초 단위 계수(86400, 3600, 60, 1)에 곱해 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    # 정규식으로 앞뒤 공백 허용, d→h→m→s 순서 및 각 단위 1회 출현 엄격 검증
    m = re.fullmatch(r'\s*(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?\s*', s)
    if not m or all(v is None for v in m.groups()):
        raise ValueError(f"Invalid duration format: {s!r}")

    d, h, mi, se = m.groups()
    return (int(d) * 86400 if d else 0) + \
           (int(h) * 3600 if h else 0) + \
           (int(mi) * 60 if mi else 0) + \
           (int(se) if se else 0)
```