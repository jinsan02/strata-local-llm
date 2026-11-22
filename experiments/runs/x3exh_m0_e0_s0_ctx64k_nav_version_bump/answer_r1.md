수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release의 첫 번째, 두 번째, 세 번째 숫자를 1 올리고 이후 숫자를 0으로 설정한다.
- 올릴 자리가 release 길이보다 긴 경우 0을 채워 늘린다 (예: `1` → micro → `1.0.1`).
- epoch는 유지하고, pre/post/dev/local은 모두 버린다.
- 유효하지 않은 `part` 값은 `ValueError`를 던진다.
- `Version.from_parts`를 사용해 새 `Version` 객체를 반환하므로 원래 객체는 불변이다.