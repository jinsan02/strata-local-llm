기존 테스트 전체(51524건)가 통과했습니다.

**수정 내용:**
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.
- `part`가 `"major"`이면 release의 첫 번째 숫자를 1 올리고, `"minor"`이면 두 번째, `"micro"`이면 세 번째를 1 올린 뒤 뒤의 숫자들을 모두 0으로 만듭니다.
- release 길이가 부족하면 0을 채워 늘립니다 (예: `1` → micro → `1.0.1`).
- pre/post/dev/local 세그먼트는 모두 버리고, epoch는 그대로 유지합니다.
- 유효하지 않은 `part` 값은 `ValueError`를 던집니다.
- 원래 객체는 불변이며 새 `Version` 인스턴스를 반환합니다.