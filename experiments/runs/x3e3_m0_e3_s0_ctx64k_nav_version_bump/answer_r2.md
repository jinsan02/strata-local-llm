수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

**변경 내용:**
- `micro` property 뒤(약 1112번째 줄)에 `bump` 메서드 추가
- `part` 가 `"major"`·`"minor"`·`"micro"` 외의 값이면 `ValueError` 발생
- 해당 인덱스의 release 숫자를 1 올리고, 뒤의 숫자들을 모두 0 으로 설정
- release 길이가 부족하면 0 을 채워 확장 (예: `"1"` → micro → `"1.0.1"`)
- epoch 는 그대로 유지하고, pre/post/dev/local 은 모두 버림
- 원래 객체는 불변이며 새 `Version` 인스턴스를 반환