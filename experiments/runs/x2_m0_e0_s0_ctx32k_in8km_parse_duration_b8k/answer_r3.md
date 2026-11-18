### 구현 개요
1. 양끝 공백을 제거하고 빈 문자열이면 즉시 `ValueError` 발생.
2. `re.findall(r"(\d+)([dhms])", s)`로 모든 `[숫자][단위]` 쌍을 추출. 단위가 하나도 없거나 숫자만 있는 경우(예: `"123"`) 에러 처리.
3. 추출된 쌍들을 다시 조인한 문자열이 원래 입력과 정확히 일치하는지 비교하여, 내부 공백이나 단위 외 문자/숫자가混入되었는지 검증.
4. 순서(`d→h→m→s`)와 중복을 방지하기 위해 각 단위의 고정 인덱스를 비교하며, 위배 시 `ValueError` 발생.
5. 지정된 시간 상수(`86400, 3600, 60, 1`)를 곱해 합산 후 정수 반환.

### 최종 코드
```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("Empty string")
        
    pairs = re.findall(r"(\d+)([dhms])", s)
    if not pairs:
        raise ValueError("No valid duration units found")
        
    # 숫자-단위 조합 외의 문자나 순서 섞임, 내부 공백 등을 원천 차단
    if "".join(f"{num}{unit}" for num, unit in pairs) != s:
        raise ValueError("Invalid format")
        
    unit_order = {"d": 0, "h": 1, "m": 2, "s": 3}
    unit_secs = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    
    last_idx = -1
    total = 0
    for num_str, unit in pairs:
        curr_idx = unit_order[unit]
        if curr_idx <= last_idx:
            raise ValueError("Units out of order or duplicated")
        total += int(num_str) * unit_secs[unit]
        last_idx = curr_idx
        
    return total
```