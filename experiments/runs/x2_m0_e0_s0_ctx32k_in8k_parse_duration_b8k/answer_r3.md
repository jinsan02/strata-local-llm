### 설명
1. 앞뒤 공백을 제거하고 빈 문자열인 경우 즉시 `ValueError` 발생.
2. 지정한 단위(`d, h, m, s`)에 순서 번호와 초 환산 계수를 매핑한 딕셔너리를 준비.
3. 문자열을 앞에서부터 순회하며 숫자 블록과 다음 단위를 구분:
   - 숫자만 있고 끝나는 경우 → `ValueError` (단위 누락)
   - 지정된 단위 외의 문자가 등장하거나 내부 공백이 있는 경우 → `ValueError`
   - 등장한 단위의 순서 번호가 직전 단위보다 작거나 같은 경우(순서 위반 또는 중복) → `ValueError`
4. 조건을 모두 통과하면 각 항목을 초 단위로 환산해 합산하고 반환.

### 코드
```python
def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")

    unit_map = {'d': (0, 86400), 'h': (1, 3600), 'm': (2, 60), 's': (3, 1)}
    i, n = 0, len(s)
    last_pri, total = -1, 0

    while i < n:
        if not s[i].isdigit():
            raise ValueError("숫자 또는 지정된 단위 외의 문자가 포함되어 있습니다.")
        
        j = i
        while j < n and s[j].isdigit():
            j += 1
            
        if j == n:
            raise ValueError("숫자만 있고 단위가 없습니다.")
            
        unit = s[j]
        if unit not in unit_map:
            raise ValueError(f"알 수 없는 단위 '{unit}'입니다.")
            
        pri, factor = unit_map[unit]
        if pri <= last_pri:
            raise ValueError("단위 순서가 잘못되었거나 중복되었습니다.")
            
        last_pri = pri
        total += int(s[i:j]) * factor
        i = j + 1
        
    return total
```