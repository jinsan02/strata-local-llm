수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다. 주요 변경 내용:

- `"major"` · `"minor"` · `"micro"` 중 하나를 받아 해당 release 인덱스를 1 올리고 뒤는 0으로 채움
- 올라갈 자리가 없으면 release 길이를 자동 확장 (예: `1` → micro → `1.0.1`)
- epoch는 유지, pre/post/dev/local은 모두 버림
- 잘못된 `part` 값이면 `ValueError` 발생
- 원래 객체는 불변이고 새 `Version` 반환 (`__replace__` 사용)