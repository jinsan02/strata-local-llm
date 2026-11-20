수정 사항을 요약하면 다음과 같습니다:

- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.
- `"major"` / `"minor"` / `"micro"` 인자에 따라 release 튜플의 첫 · 둘째 · 셋째 숫자를 1 올리고, 이후 숫자는 모두 0으로 만듭니다.
- 올릴 자리가 현재 release 길이보다 크면 해당 자리까지 0을 채워 늘립니다 (예: `(1,)` → micro → `(1, 0, 1)`).
- epoch는 그대로 유지하고, pre/post/dev/local은 `Version.from_parts()`의 기본값(None)으로 인해 자동으로 버려집니다.
- 유효하지 않은 part 값은 `ValueError`를 던집니다.
- 기존 객체는 변경되지 않고 새 `Version` 인스턴스를 반환합니다.