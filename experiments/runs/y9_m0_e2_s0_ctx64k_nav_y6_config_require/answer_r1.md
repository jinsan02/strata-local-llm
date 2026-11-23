`src/flask/config.py`에 `Config.require` 메서드를 추가했다. 이 메서드는:

- 주어진 문자열 키들의 값을 담은 새 `dict`를 반환하며, 키 순서와 중복 제거를 처리한다.
- 없는 키나 `allow_none=False`일 때 값이 `None`인 키가 있으면 정렬된 키 목록을 포함한 `KeyError`를 던진다.
- 키가 없으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError`를 던진다.