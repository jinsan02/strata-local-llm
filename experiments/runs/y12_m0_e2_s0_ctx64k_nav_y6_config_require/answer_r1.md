`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했다. 주요 동작:

- 인자 없이 호출 시 `TypeError`
- 문자열이 아닌 키가 있으면 `TypeError`
- 중복 키는 한 번만 처리, 순서는 인자 순서 유지
- 없는 키 또는 `allow_none=False`일 때 값이 `None`인 키는 `KeyError` 던짐. 예외 메시지는 `"Missing required config keys: "` 뒤에 정렬된 누락 키들을 `", "`로 이음
- 모든 키가 유효하면 해당 키-값 쌍을 담은 새 `dict` 반환 (인자 순서 유지)