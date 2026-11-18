### 접근 방식
1. `strip()`로 앞뒤 공백을 제거하고, 빈 문자열이면 즉시 `ValueError` 발생.
2. 고정 순서(`d → h → m → s`)와 각 단위 최대 1회 출력을 강제하는 정규식으로 전체 매칭 검증.
   - 패턴 내부에서 각 단위가 한 번씩만 정의되어 있어 **순서 위반**과 **단위 중복**을 자연스럽게 차단합니다.
   - 숫자+단위 조합 외의 문자(내부 공백, 단위 누락, 알 수 없는 글자 등)는 매칭 실패로 처리됩니다.
3. 매칭되더라도 모든 그룹이 `None`이면 단위가 하나도 없으므로 `ValueError`.
4. 추출된 숫자를 해당 초 단위 계수(`86400, 3600, 60, 1`)에 곱해 합산 후 반환.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty duration string")
        
    match = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', s)
    if not match or all(g is None for g in match.groups()):
        raise ValueError("Invalid duration format")
        
    d, h, m, sec = match.groups()
    return int(d or 0) * 86400 + \
           int(h or 0) * 3600 + \
           int(m or 0) * 60 + \
           int(sec or 0)
```