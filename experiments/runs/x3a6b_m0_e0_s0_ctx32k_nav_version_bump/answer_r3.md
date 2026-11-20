수정 사항 요약:

**파일**: `src/packaging/version.py`

**변경 내용**: `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.

- `"major"`: release[0] + 1, 나머지 0으로
- `"minor"`: release[1] + 1, 뒤쪽 0으로 (없으면 0 채움)
- `"micro"`: release[2] + 1, 뒤쪽 0으로 (없으면 0 채움)
- epoch 유지, pre/post/dev/local 모두 버림
- 잘못된 part 값은 `ValueError` 던짐
- 원래 객체 불변, 새 `Version` 반환