수정 내용을 요약하면:

`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다. 이 메서드는:
- `part` 가 `"major"`이면 release 의 첫 번째 숫자를 1 올리고, `"minor"`이면 두 번째, `"micro"`이면 세 번째 숫자를 1 올린다.
- 올릴 자리가 없으면 0 을 채워 해당 자리까지 확장한다.
- 그 뒤의 모든 release 숫자는 0 으로 만든다.
- epoch 는 그대로 유지하고, pre/post/dev/local 은 모두 버린다.
- 유효하지 않은 `part` 값에 대해서는 `ValueError` 를 던진다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.