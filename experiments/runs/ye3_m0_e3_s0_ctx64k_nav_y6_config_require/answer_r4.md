`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다.

**주요 동작:**
- `*keys`로 받은 문자열 키들의 값을 담은 새 `dict`를 반환 (인자 순서 유지, 중복 제거)
- 없는 키가 있으면 `KeyError` 발생 (메시지: `"Missing required config keys: A, B"` 형식, 키는 정렬)
- `allow_none=False`일 때 값이 `None`인 키도 없는 것으로 취급
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 발생