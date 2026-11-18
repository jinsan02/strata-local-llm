### 구현 요약
1. `strip()`로 앞뒤 공백을 제거한 후 빈 문자열이면 즉시 `ValueError` 발생.
2. 정규식 `r'(\d+)([dhms])'`로 모든 `[숫자][단위]` 쌍을 추출.
3. 추출된 쌍으로 원문을 재구성해 비교. 내부 공백이나 존재하지 않는 글자가 있으면 `ValueError`.
4. 지정된 순서(`d → h → m → s`)로 차례대로 매칭하며 계산. 현재 단위가 나오지 않으면 넘어가고, 순서가 어긋나거나 중복되면 `ValueError` 발생.
5. 모든 쌍이 소모되었는지 확인 후 총 초를 반환.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열 또는 공백만 포함됩니다.")

    pairs = re.findall(r'(\d+)([dhms])', s)
    if not pairs:
        raise ValueError("숫자-단위 쌍이 없습니다.")

    # 원본 문자열 재구성 검사 (내부 공백/알파벳 등 유효성 검증)
    if ''.join(f"{num}{unit}" for num, unit in pairs) != s:
        raise ValueError("형식이 올바르지 않습니다.")

    units_order = ['d', 'h', 'm', 's']
    multipliers = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    total = 0
    idx = 0

    for unit in units_order:
        if idx < len(pairs) and pairs[idx][1] == unit:
            total += int(pairs[idx][0]) * multipliers[unit]
            idx += 1
        elif idx >= len(pairs):
            break
        else:
            raise ValueError("단위 순서가 위반되었거나 중복되었습니다.")

    if idx != len(pairs):
        raise ValueError("알 수 없는 단위이거나 형식이 잘못되었습니다.")

    return total
```