## 설명
1. 입력 문자열의 앞뒤 공백을 제거한 후, `re.fullmatch`로 정규식 패턴과 완전히 일치하는지 검사합니다.
2. 패턴 `r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$'` 은 `d→h→m→s` 순서를 강제하며, 각 단위는 최대 한 번 등장하거나 생략될 수 있게 합니다.
3. 정규식 매칭 후 모든 capturing 그룹이 `None` 이면 단위 없이 숫자만 입력된 경우이므로 `ValueError` 를 발생시킵니다.
4. 매칭된 숫자들을 정수로 변환해 각각의 초 단위 계수(`86400, 3600, 60, 1`)와 곱한 후 합산하여 반환합니다.

## 최종 코드
```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    
    # d, h, m, s 순서 강제 및 각 단위 최대 1회 등장 허용
    pattern = r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$'
    match = re.fullmatch(pattern, s)
    
    if not match or all(g is None for g in match.groups()):
        raise ValueError(f"Invalid duration format: {s!r}")
        
    d_val, h_val, m_val, s_val = (int(v) if v else 0 for v in match.groups())
    
    return d_val * 86400 + h_val * 3600 + m_val * 60 + s_val
```