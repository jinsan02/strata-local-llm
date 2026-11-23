`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했다.

- 키가 없으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 던짐
- 중복 키는 첫 등장만 포함하고 인자 순서 유지
- 없는 키 또는 `allow_none=False`일 때 값이 `None`인 키는 누락으로 간주
- 누락 키가 있으면 정렬된 누락 키들을 `"Missing required config keys: A, B"` 형식의 `KeyError`로 한 번에 알림
- 모든 키가 유효하면 해당 키-값 쌍을 담은 새 `dict` 반환