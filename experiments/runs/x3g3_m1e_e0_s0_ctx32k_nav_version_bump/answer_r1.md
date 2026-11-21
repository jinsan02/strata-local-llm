수정 완료했습니다. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

주요 변경 사항:
- `_trim_release` 메서드 뒤에 `bump` 메서드 추가
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 발생
- 해당 인덱스의 release 숫자를 1 증가시키고, 뒤의 모든 숫자를 0으로 설정
- release 길이가 부족하면 0을 채워 확장
- epoch는 유지하고, pre/post/dev/local은 모두 버림
- 원래 객체는 변경하지 않고 새 `Version` 인스턴스 반환