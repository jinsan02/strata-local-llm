`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

주요 변경 사항:
- `part` 인자가 `"major"`, `"minor"`, `"micro"` 중 하나인지 검증하고, 아니면 `ValueError`를 발생시킵니다.
- 해당 인덱스의 release 숫자를 1 증가시키고, 그 뒤의 숫자는 모두 0으로 초기화합니다.
- release 길이가 부족하면 0을 채워 필요한 길이까지 늘립니다.
- epoch는 그대로 유지하고, pre, post, dev, local 세그먼트는 모두 제거합니다.
- 기존 객체는 수정하지 않고 새 `Version` 객체를 반환합니다.