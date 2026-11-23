`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했다. 이 메서드는:
- 주어진 키들의 값을 담은 새 `dict`를 인자 순서대로 반환한다.
- 중복 키는 한 번만 처리한다.
- 없는 키나 `None` 값(`allow_none=False`)이 있으면 정렬된 키 목록과 함께 `KeyError`를 던진다.
- 키가 없으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError`를 던진다.