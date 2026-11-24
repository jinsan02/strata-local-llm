기존 테스트 파일은 수정하지 말라고 했으니, 구현만 확인하면 된다. 수정 내용을 요약하자면:

- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release 튜플의 첫 번째, 두 번째, 세 번째 요소를 1 증가시키고, 뒤의 요소들을 0으로 설정한다.
- release 길이가 부족하면 0을 채워 확장한다.
- epoch는 유지하고, pre/post/dev/local은 모두 버린다.
- 유효하지 않은 `part` 값은 `ValueError`를 던진다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.