`src/packaging/version.py`의 `Version` 클래스에 다음 두 메서드를 추가했다:

1. **`_bump_release(self, part: str) -> tuple[int, ...]`** — release 튜플에서 지정된 부분(`"major"`, `"minor"`, `"micro"`)을 1 올리고 뒤의 요소를 0으로 만드는 내부 헬퍼. 유효하지 않은 part면 `ValueError`.

2. **`bump(self, part: str) -> Version`** — public 메서드. `_bump_release`로 새 release를 만들고, epoch는 유지한 채 pre/post/dev/local은 모두 버린 새 `Version`을 반환. docstring에 예제 포함.