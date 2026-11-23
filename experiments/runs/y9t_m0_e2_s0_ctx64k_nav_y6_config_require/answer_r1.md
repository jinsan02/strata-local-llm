수정을 마쳤습니다. `src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다.

구현 내용:
- 인자가 없으면 `TypeError` 던짐
- 문자열이 아닌 키가 있으면 `TypeError` 던짐
- 없는 키나 `allow_none=False`일 때 값이 `None`인 키를 `missing` 리스트에 수집
- `missing`이 있으면 정렬하여 `"Missing required config keys: A, B"` 형식의 `KeyError` 던짐
- 키 순서대로 결과를 담은 `dict`를 반환하되, 중복 키는 한 번만 담음