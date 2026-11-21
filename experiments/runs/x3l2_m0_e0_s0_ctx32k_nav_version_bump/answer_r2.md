수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`/`"minor"`/`"micro"`일 때 각각 release 의 첫 번째/두 번째/세 번째 숫자를 1 올리고 뒤를 0 으로 채운다.
- release 길이가 부족하면 0 으로 확장한다.
- epoch 는 유지하고, pre/post/dev/local 은 모두 버린다.
- 잘못된 `part` 값은 `ValueError` 를 던진다.
- 원래 객체는 변경하지 않고 새 `Version` 인스턴스를 반환한다.