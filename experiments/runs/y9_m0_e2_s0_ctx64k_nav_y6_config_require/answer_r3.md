`src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다.

**추가된 내용:**
- `require(self, *keys: str, allow_none: bool = False) -> dict[str, Any]` 메서드
- 인자 순서대로 키를 deduplicate 하며 해당 값들을 담은 새 dict 반환
- 없는 키 또는 `allow_none=False`일 때 값이 `None`인 키는 `KeyError` 발생
- 예외 메시지: `"Missing required config keys: "` + 정렬된 누락 키 목록 (`, ` 구분)
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 발생
- 기존 설정 값은 수정하지 않으며 기존 동작은 변경되지 않음