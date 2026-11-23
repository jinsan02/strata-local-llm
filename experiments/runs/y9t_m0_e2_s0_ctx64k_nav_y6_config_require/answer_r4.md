수정 완료. `src/flask/config.py`의 `Config` 클래스에 `require(*keys: str, allow_none: bool = False) -> dict` 메서드를 추가했습니다.

주요 동작:
- **키 검증**: 키가 없으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError`
- **중복 키**: 같은 키를 여러 번 주면 한 번만 결과에 포함 (인자 순서 유지)
- **누락 키**: `KeyError` 던지며, 메시지는 `"Missing required config keys: "` 뒤에 정렬된 누락 키들을 `", "`로 이어붙임 (예: `"Missing required config keys: A, B"`)
- **allow_none**: `False`일 때 값이 `None`인 키도 누락으로 간주
- 기존 테스트 19개 모두 통과.