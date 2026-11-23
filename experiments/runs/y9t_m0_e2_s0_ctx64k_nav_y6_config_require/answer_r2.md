수정 완료. `src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했다.

주요 동작:
- `*keys` 인자로 전달된 키들의 값을 담은 새 `dict`를 순서대로 반환
- 중복 키는 한 번만 처리
- 없는 키나 `allow_none=False`일 때 값이 `None`인 키가 있으면 `KeyError` 발생
- 예외 메시지는 `"Missing required config keys: "` 뒤에 정렬된 누락 키들을 `", "`로 이어붙인 형식
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 발생