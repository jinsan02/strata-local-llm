### 설명
1. `strip()`로 양끝 공백을 제거하고 빈 문자열이면 즉시 `ValueError` 발생
2. 정규식 `^(\d+d)?(\d+h)?(\d+m)?(\d+s)?$` 로 **d→h→m→s 순서**, **각 단위 최대 1회 등장**, **단위 생략 불가**를 엄격하게 검증
3. 매칭된 그룹에서 숫자와 단식을 분리해 초 단위 환산 후 합산
4. 형식 불일치(내부 공백, 단위 누락/중복/순서 뒤섞임, 미지원 문자 등) 시 정규식 실패로 `ValueError` 발생

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty string")
        
    match = re.fullmatch(r'^(\d+d)?(\d+h)?(\d+m)?(\d+s)?$', s)
    if not match:
        raise ValueError("Invalid format")
        
    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    return sum(int(g[:-1]) * units[g[-1]] for g in match.groups() if g)
```