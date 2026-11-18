주어진 조건을 엄격히 만족하기 위해 `re.fullmatch` 를 사용한 정규식 기반 파싱을 구현했습니다. 각 단위가 최대 한 번만 등장하고, 고정된 순서 `(d, h, m, s)` 로만 매칭되도록 설계하였으며, 매칭 실패 시 `ValueError` 를 발생시킵니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열은 유효하지 않습니다.")
        
    # d, h, m, s 순서로 각각 0 또는 1회 등장하는 패턴
    match = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not match:
        raise ValueError("유효하지 않은 기간 형식입니다.")
        
    d, h, m, sec = match.groups()
    
    return (int(d) * 86400 if d else 0) + \
           (int(h) * 3600 if h else 0) + \
           (int(m) * 60 if m else 0) + \
           (int(sec) if sec else 0)
```

### 동작 특징
- **정규식 `(?:(\d+)d)?(...)`**: 각 단위 그룹은 `?` 로 인해 0회 또는 1회만 허용하며, 고정된 순서로 작성되어 순서 위반/중복을 즉시 차단합니다.
- **단위 누락 및 알 수 없는 문자 차단**: `\d+` 에 영문/숫자 외 문자가 오거나 단위 없이 숫자만 있으면 `fullmatch` 가 `None` 을 반환해 `ValueError` 를 일으킵니다.
- **공백 처리**: `.strip()` 으로 양끝 공백을 제거하고, 내부 공백은 정규식 매칭 실패로 간주합니다.