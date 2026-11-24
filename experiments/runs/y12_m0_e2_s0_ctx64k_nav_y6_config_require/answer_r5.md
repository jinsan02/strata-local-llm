`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했다. 주요 동작:

- 인자로 받은 키들의 값을 담은 새 `dict`를 반환하며, 키 순서는 인자 순서를 유지한다.
- 중복 키는 한 번만 담는다.
- 없는 키가 있으면 `KeyError`를 던지며, 메시지 형식은 `"Missing required config keys: A, B"` (키 정렬, `, ` 구분).
- `allow_none=False`일 때 값이 `None`인 키도 없는 것으로 취급한다.
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError`를 던진다.