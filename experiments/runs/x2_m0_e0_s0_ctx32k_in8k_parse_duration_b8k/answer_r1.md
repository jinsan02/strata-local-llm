### 요약 설명
1. `strip()`로 앞뒤 공백을 제거한 후 빈 문자열이면 즉시 `ValueError` 발생.
2. `re.fullmatch`로 입력값 전체를 검증합니다. 정규식 구조 `(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:([0-9]+)s)?`는 단위的出现 순서(`d→h→m→s`)와 최대 1회 등장, 숫자만 허용을 엄격히 강제합니다. 이 구조로 인해 중간 공백, 순서 위반, 중복 단위, 알 수 없는 단위, 단위 결손이 모두 매치 실패로 처리되어 `ValueError`를 유발합니다.
3. 매칭된 그룹에서 숫자만을 추출해 `or 0`으로 기본값 처리한 뒤, 각 단위의 초 환산 계수(`86400, 3600, 60, 1`)를 적용해 합산 반환합니다.

### 최종 코드
```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열은 허용되지 않습니다.")
        
    # d, h, m, s 순서로 각 단위 최대 1회 등장. 숫자는 0 이상 정수만 허용.
    m = re.fullmatch(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:([0-9]+)s)?', s)
    if not m:
        raise ValueError(f"잘못된 형식입니다: {s!r}")
        
    days = int(m.group(1) or 0)
    hours = int(m.group(2) or 0)
    minutes = int(m.group(3) or 0)
    seconds = int(m.group(4) or 0)
    
    return days * 86_400 + hours * 3_600 + minutes * 60 + seconds
```