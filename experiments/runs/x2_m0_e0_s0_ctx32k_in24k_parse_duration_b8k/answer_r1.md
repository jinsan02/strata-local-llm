### 설명
1. `strip()`로 앞뒤 공백을 제거한 후 빈 문자열이면 `ValueError` 발생.
2. 정규식 `(\d+)([dhms])` 로 `숫자+단위` 쌍만 추출합니다. 이 방식은 알 수 없는 단위나 숫자/단위가 섞인 경우 매칭에서 자연스럽게 배제됩니다.
3. 추출된 쌍들을 다시 조인한 결과가 원문과 완전히 일치하는지 확인합니다. 이를 통해 내부 공백, 단위 누락, 임의의 특수문자 등을 `ValueError` 로 걸러냅니다.
4. 추출된 단위 목록이 `[d, h, m, s]` 의 순서를 지키면서 중복 없이 나타나는지 검증합니다.
5. 검증 통과 시 각 단위에 해당하는 초 단위(86400, 3600, 60, 1) 곱해 합산하여 반환합니다.

```python
import re

def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열입니다.")
        
    # 숫자+단위 쌍만 추출 (d, h, m, s 외의 글자는 매칭 불가)
    tokens = re.findall(r'(\d+)([dhms])', s)
    
    # 전체 문자열이 추출된 쌍들만으로 구성되었는지 검증
    # → 내부 공백, 단위 없는 숫자, 임의의 추가 문자 등을 ValueError로 처리
    if "".join(f"{n}{u}" for n, u in tokens) != s:
        raise ValueError("형식이 올바르지 않습니다.")
    if not tokens:
        raise ValueError("유효한 기간 단위가 없습니다.")
        
    # 순서(d→h→m→s)와 중복 체크
    units = [u for _, u in tokens]
    if len(units) != len(set(units)) or units != sorted(units, key=lambda u: 'dhms'.index(u)):
        raise ValueError("단위는 d, h, m, s 순서대로 하나씩만 올 수 있습니다.")
        
    multipliers = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    return sum(int(n) * multipliers[u] for n, u in tokens)
```