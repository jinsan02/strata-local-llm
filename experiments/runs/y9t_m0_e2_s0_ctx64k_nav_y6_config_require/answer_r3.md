`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다. 주요 동작:

- `*keys`로 받은 설정 키들의 값을 담은 새 `dict`를 인자 순서대로 반환 (중복 키는 한 번만 포함)
- 없는 키가 있으면 `KeyError`를 던지며, 메시지는 `"Missing required config keys: "` 뒤에 정렬된 키들을 `", "`로 연결
- `allow_none=False`일 때 값이 `None`인 키도 없는 것으로 간주
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 던짐
- 기존 동작은 변경하지 않음

기존 테스트 19개 모두 통과.