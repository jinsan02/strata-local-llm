수정 내용:
- `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함
- `_trim_release` 메서드 뒤 (라인 1138 이후) 에 삽입
- `part` 가 `"major"`/`"minor"`/`"micro"` 외에는 `ValueError` 던짐
- 해당 release 인덱스를 1 증가시키고 뒤쪽 인덱스를 0 으로 채움
- release 길이가 부족하면 0 을 채워 늘림
- epoch 는 유지, pre/post/dev/local 은 모두 버림
- 새 `Version` 객체를 반환 (원본 불변)
- docstring 에 doctest 예제 포함