기존 테스트 51,524건 모두 통과.

수정 내용:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.
- `micro` property 뒤, `_trim_release` 메서드 앞에 삽입.
- `part`가 `"major"`/`"minor"`/`"micro"`인 경우 해당 release 인덱스를 1 올리고, 뒤의 모든 인덱스를 0으로 설정. release 길이가 부족하면 0으로 채워 확장.
- epoch는 유지, pre/post/dev/local은 모두 버림.
- 잘못된 `part` 값은 `ValueError` 던짐.
- 불변 객체 유지 (새 `Version` 반환).