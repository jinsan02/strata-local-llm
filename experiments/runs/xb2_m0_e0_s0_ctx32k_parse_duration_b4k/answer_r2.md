`re.fullmatch`를 사용해 전체 문자열이 `(\d+d)?(\d+h)?(\d+m)?(\d+s)?` 패턴과 정확히 일치하는지 검증합니다. 이 정규식은 각 단위가 최대 한 번 등장하며, 반드시 `d → h → m → s` 순서만 허용하도록 설계되었습니다. 앞뒤 공백은 `.strip()`으로 제거하고, 매칭 실패 또는 빈 문자열은 `ValueError`를 발생시킵니다. 매칭된 그룹에서 단위 문자를 제외해 정수화한 뒤 곱하여 합산합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    # (숫자+단위) 형태가 d, h, m, s 순서로 최대 한 번씩만 나타나야 함
    match = re.fullmatch(r'(\d+d)?(\d+h)?(\d+m)?(\d+s)?', s)
    if not match:
        raise ValueError(f"잘못된 형식: '{s}'")
        
    total = 0
    factors = [86400, 3600, 60, 1]  # d, h, m, s 초 단위
    
    for group in match.groups():
        if group is not None:
            num = int(group[:-1])       # 단위 문자 제거 후 정수화
            idx = 'dhs'.find(group[-1]) # 단위에 맞는 인덱스로 시간 배율 매핑
            total += num * factors[idx]
            
    return total
```