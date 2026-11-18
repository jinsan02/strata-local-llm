`src/packaging/version.py`의 `Version` 클래스 내 `_trim_release` 메서드 앞에 `bump(part: str) -> Version` 메서드를 추가했습니다.

구현 내용:
- `part`가 `"major"`, `"minor"`, `"micro"`일 때 각각 release의 1, 2, 3번째 숫자를 1 증가시키고 그 뒤의 모든 숫자를 0으로 만듦
- 요청한 자리가 release에 없으면 0을 채워 해당 길이까지 확장 (예: `1` → micro → `1.0.1`)
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버림 (`__replace__`의 기본값 + 명시적 `None`)
- 그 밖의 `part` 값(대소문자 포함)은 `ValueError` 던짐
- 원래 객체는 변경되지 않고 새 `Version` 반환