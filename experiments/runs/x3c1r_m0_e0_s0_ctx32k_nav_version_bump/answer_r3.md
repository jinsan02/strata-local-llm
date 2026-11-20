수정 완료했습니다.

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다. 주요 동작:
- `"major"`(index 0), `"minor"`(index 1), `"micro"`(index 2) 중 하나여야 하며, 나머지는 `ValueError` 발생
- 해당 인덱스의 값을 1 증가시키고 이후 모든 release 요소를 0으로 초기화
- 인덱스가 release 길이보다 크면 해당 위치까지 0으로 채워 확장
- epoch는 유지하고, pre/post/dev/local은 모두 버림
- 새 `Version.from_parts`로 복사본을 반환하여 원래 객체 불변성 유지