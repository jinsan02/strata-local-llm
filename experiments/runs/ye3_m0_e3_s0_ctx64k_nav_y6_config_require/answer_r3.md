`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다.

**변경 내용:**
- `Config` 클래스에 `require(self, *keys: str, allow_none: bool = False) -> dict[str, Any]` 메서드 추가
- 키가 없거나 `allow_none=False`일 때 값이 `None`이면 `KeyError` 발생 (메시지: `"Missing required config keys: A, B"` 형식, 키는 정렬됨)
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 발생
- 중복 키는 한 번만 처리하고 인자 순서 유지
- 기존 동작은 변경 없음