`src/flask/config.py` 의 `flask.Config` 클래스에 `require(*keys, allow_none=False)` 메서드를 추가했다. 이 메서드는:

- 주어진 문자열 키들의 값을 담은 새 `dict` 를 반환하며, 키는 인자 순서를 유지하고 중복은 제거한다.
- 키를 하나도 주지 않거나 문자열이 아닌 키가 있으면 `TypeError` 를 던진다.
- 없는 키나 `allow_none=False` 일 때 `None` 인 값의 키가 있으면, 정렬된 누락 키 목록을 포함한 `KeyError` 를 한 번에 던진다.