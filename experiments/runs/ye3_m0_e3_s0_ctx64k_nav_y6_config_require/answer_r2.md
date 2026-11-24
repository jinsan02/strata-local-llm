수정 완료했습니다. `src/flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다.

**변경 사항 요약:**
- `Config` 클래스에 `require(self, *keys: str, allow_none: bool = False) -> t.Dict[str, t.Any]` 메서드 추가
- 키가 없으면 정렬된 누락 키 목록을 담은 `KeyError` 발생 (첫 번째에서 멈추지 않고 모두 수집)
- `allow_none=False`일 때 값이 `None`인 키도 누락으로 간주
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 발생
- 같은 키가 중복으로 주어지면 한 번만 담고, 인자 순서 유지
- 기존 설정 값은 변경하지 않음