수정 내용을 요약하면:

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다. 이 메서드는:
- `part` 가 `"major"`이면 release 의 첫 번째 숫자를 1 올리고, `"minor"`이면 두 번째, `"micro"`이면 세 번째 숫자를 1 올린 뒤 뒤의 숫자를 모두 0 으로 만든다.
- 올릴 자리가 release 에 없으면 0 을 채워 해당 길이까지 확장한다.
- pre/post/dev/local 은 모두 None 으로 버리고 epoch 는 그대로 유지한다.
- 원래 객체는 변경하지 않고 새 `Version` 인스턴스를 반환한다.
- 유효하지 않은 `part` 값이면 `ValueError` 를 던진다.