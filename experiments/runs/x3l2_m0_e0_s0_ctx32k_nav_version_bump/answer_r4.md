수정 내용을 요약하면:

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 일 때 각각 release 튜플의 0번째, 1번째, 2번째 요소를 1 증가시키고, 그 뒤의 요소를 모두 0 으로 설정한다.
- 인덱스가 현재 release 길이보다 크면 0 을 채워 늘린다.
- epoch 는 유지하고, pre/post/dev/local 은 모두 None 으로 버린다.
- 그 밖의 `part` 값은 `ValueError` 를 던진다.
- 원래 객체는 변경하지 않고 새 `Version` 인스턴스를 반환한다.