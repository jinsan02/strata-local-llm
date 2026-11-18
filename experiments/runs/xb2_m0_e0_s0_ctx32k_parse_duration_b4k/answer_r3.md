`re` 모듈을 사용해 고정된 순서와 형식을 검증하고 그룹화된 숫자를 추출하는 방식이 가장 명확합니다. 정규식은 각 단위가 `숫자 + 단위` 쌍으로만 구성되며, 누락 시에는 해당 그룹이 매칭되지 않도록 설계합니다. 빈 문자열, 공백, 단위 누락/중복/순서불일치/알 수 없는 문자는 모두 매칭 실패로 처리해 `ValueError`를 발생시킵니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")

    # d, h, m, s 순서대로 숫자+단위 쌍이 최대 한 번씩 나올 수 있음
    match = re.match(r'^((\d+)d)?((\d+)h)?((\d+)m)?((\d+)s)?$', s)
    if not match:
        raise ValueError("형식이 올바르지 않습니다.")

    multipliers = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    total = 0
    
    # 추출된 숫자 그룹(인덱스 2,4,6,8)을 d,h,m,s 순서와 매핑하여 계산
    for num_str in (match.group(i) for i in range(2, 9, 2)):
        if num_str is not None:
            total += int(num_str) * multipliers[{'d':'d', 'h':'h', 'm':'m', 's':'s'}[num_str]]

    return total
```