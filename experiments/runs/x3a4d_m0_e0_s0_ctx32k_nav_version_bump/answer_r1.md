`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

구현 내용:
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 발생
- 해당 인덱스의 release 숫자를 1 올리고, 뒤의 숫자들은 0으로 설정
- release 길이가 부족하면 0을 채워 확장
- epoch는 유지, pre/post/dev/local은 모두 버림
- `from_parts`를 사용해 새 `Version` 객체 반환