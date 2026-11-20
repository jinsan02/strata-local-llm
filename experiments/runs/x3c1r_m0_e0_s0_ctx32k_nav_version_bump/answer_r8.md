수정을 완료했다. `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `"major"`, `"minor"`, `"micro"` 외의 값은 `ValueError` 를 던진다.
- 지정된 release 부분을 1 증가시키고 이후 부분을 모두 0 으로 만든다.
- pre/post/dev/local 은 모두 버리고 epoch 는 유지한다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.