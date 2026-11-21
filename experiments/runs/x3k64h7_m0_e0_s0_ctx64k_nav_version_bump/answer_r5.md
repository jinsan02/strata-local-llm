`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Self` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release의 첫째, 둘째, 셋째 숫자를 1 올리고 뒤를 0으로 채운다.
- 올릴 자리가 없으면 0으로 패딩하여 해당 자리까지 늘린다.
- pre/post/dev/local은 모두 버리고 epoch는 유지한다.
- 그 밖의 `part` 값은 `ValueError`를 던진다.
- `__replace__`를 활용해 새 `Version` 객체를 반환하므로 원래 객체는 불변이다.