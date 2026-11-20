수정 완료했습니다. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**변경 내용 요약:**
- `_trim_release` 메서드 다음에 `bump` 메서드 추가
- `"major"` (첫 번째), `"minor"` (두 번째), `"micro"` (세 번째) release 숫자를 각각 1 증가시키고 이후 숫자를 모두 0으로 설정
- 현재 release 길이보다 작은 인덱스를 bump할 경우 0을 채워 길이를 늘림
- epoch는 유지하고 pre/post/dev/local은 버림
- 유효하지 않은 part 값에 대해 `ValueError` 발생