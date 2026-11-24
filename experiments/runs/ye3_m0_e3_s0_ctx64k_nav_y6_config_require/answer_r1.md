`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다.

**주요 동작:**
- `*keys`로 지정된 설정 키들의 값을 담은 새 `dict`를 반환 (인자 순서 유지, 중복 키는 한 번만 포함)
- 키가 없거나 `allow_none=False`일 때 값이 `None`이면 `KeyError` 발생 (모든 누락 키를 정렬하여 한 번에 알림)
- 키가 없으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 발생
- 기존 설정 값은 수정하지 않음