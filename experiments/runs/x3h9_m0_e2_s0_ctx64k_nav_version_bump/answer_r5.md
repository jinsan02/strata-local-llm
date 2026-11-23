수정 완료.

### 변경 사항 요약

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- **메서드 위치**: `micro` property 직후, `_trim_release` 메서드 전
- **동작**:
  - `part`가 `"major"`면 release 첫째 숫자를 1 올리고, `"minor"`면 둘째, `"micro"`면 셋째를 1 올린 후 뒤의 모든 숫자를 0으로 설정
  - 올릴 자리가 release 길이보다 크면 0을 채워 확장 (예: `1` → micro → `1.0.1`)
  - epoch는 유지하고, pre/post/dev/local은 모두 버림 (예: `2!1.2.3rc1.post2.dev3+abc` → micro → `2!1.2.4`)
  - 유효하지 않은 `part` 값은 `ValueError` 발생
  - 원래 객체는 불변이며 새 `Version` 인스턴스 반환