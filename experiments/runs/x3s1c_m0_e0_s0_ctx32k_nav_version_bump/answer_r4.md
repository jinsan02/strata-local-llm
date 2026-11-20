수정을 완료했습니다. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**변경 내용 요약:**
- `Version` 클래스의 `micro` 속성 다음에 `bump` 메서드 추가
- `part` 값이 `"major"`, `"minor"`, `"micro"` 중 하나일 때 해당 인덱스의 release 숫자를 1 증가시키고 뒤의 숫자들을 0으로 설정
- release 길이가 부족하면 0을 채워 확장
- epoch는 유지하고 pre/post/dev/local은 모두 버림
- 유효하지 않은 `part` 값에 대해 `ValueError` 발생
- `__replace__`를 사용해 새 `Version` 객체 반환 (원본 불변)