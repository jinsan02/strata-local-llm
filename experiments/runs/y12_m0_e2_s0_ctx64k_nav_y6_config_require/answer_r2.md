`flask/config.py`의 `Config` 클래스에 `require` 메서드를 추가했습니다.

주요 동작:
- `keys`가 비어 있으면 `TypeError` 발생
- 문자열이 아닌 키가 있으면 `TypeError` 발생
- 중복 키 제거 후 순서 유지
- `allow_none=False`일 때 값이 `None`인 키도 누락으로 처리
- 누락된 키가 있으면 정렬된 키 목록을 포함한 `KeyError` 발생 (예: `"Missing required config keys: A, B"`)
- 모든 키가 유효하면 해당 키-값 쌍을 담은 새 `dict` 반환 (인자 순서 유지)