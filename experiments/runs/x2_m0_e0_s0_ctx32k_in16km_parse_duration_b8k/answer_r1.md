문자열의 형태를 고정된 패턴으로 매칭하면 순서, 중복, 사공백, 미단위 숫자 등을 한 번에 검증할 수 있습니다. 정규식으로 각 단위 옵션 그룹을 순차적으로 배치하고, `fullmatch`로 문자열 전체를 검제한 뒤 그룹 중 최소 하나라도 채워졌는지 확인하면 요구사항을 깔끔하게 충족합니다.

```python
import re

def parse_duration(s: str) -> int:
    """기간 문자열을 초 단위 정수로 변환합니다."""
    # 각 단위는 선택적이며 고정 순서로만 등장 가능. 내부 공백이나 미등록 문자는 매칭 실패.
    m = re.fullmatch(r'^\s*(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?\s*$', s)
    if not m or all(v is None for v in m.groups()):
        raise ValueError("Invalid duration string")
        
    days, hours, mins, secs = m.groups()
    total = 0
    if days:   total += int(days) * 86400
    if hours:  total += int(hours) * 3600
    if mins:   total += int(mins) * 60
    if secs:   total += int(secs)
    return total
```