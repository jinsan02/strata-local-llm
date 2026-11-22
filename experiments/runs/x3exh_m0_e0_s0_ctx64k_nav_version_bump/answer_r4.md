수정 내용을 요약하면:

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`이면 release의 첫 번째 숫자를 1 올리고 뒤를 0으로, `"minor"`이면 두 번째, `"micro"`이면 세 번째를 1 올리고 뒤를 0으로 만듭니다.
- release 길이가 부족한 경우 0을 채워 해당 위치까지 확장합니다 (예: `1` → micro → `1.0.1`).
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버립니다 (예: `2!1.2.3rc1.post2.dev3+abc` → micro → `2!1.2.4`).
- 유효하지 않은 `part` 값은 `ValueError`를 던집니다.
- `Version.from_parts()`를 사용해 새 객체를 반환하므로 원래 객체는 변하지 않습니다.