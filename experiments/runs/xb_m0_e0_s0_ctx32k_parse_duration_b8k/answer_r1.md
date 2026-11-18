주어진 조건을 정확히 반영하기 위해 정규식으로 숫자-단위 쌍을 추출하고, 재조립하여 불필요한 문자나 공백이 있는지 검사합니다. 단위 순서와 연속성(중간 생략 방지)은 인덱스 범위로 검증합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    # 숫자와 단위를 매칭 (단: d, h, m, s 만 허용)
    matches = re.findall(r'(\d+)([dhms])', s)
    
    # 매칭된 쌍을 이어붙인 것이 원본과 완전히 일치해야 함
    # (앞뒤 공백 제외, 내부 공백/알 수 없는 숫자/단위 차단)
    if ''.join(f"{n}{u}" for n, u in matches) != s:
        raise ValueError("형식이 올바르지 않습니다.")
        
    if not matches:
        raise ValueError("유효한 기간 표현이 없습니다.")
        
    units = [u for _, u in matches]
    unit_map = {'d': 0, 'h': 1, 'm': 2, 's': 3}
    weights = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    
    indices = [unit_map[u] for u in units]
    
    # 1. strict increasing order (순서 위반 차단)
    # 2. 연속성 검사 (중간 단위 생략 차단: ex. "1d5s" 금지)
    if indices != list(range(indices[0], indices[0] + len(units))):
        raise ValueError("단위 순서가 잘못되었거나 중간 단위가 생략되었습니다.")
        
    return sum(int(num) * weights[unit] for num, unit in matches)
```