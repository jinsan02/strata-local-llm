수정 내용 요약:

- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고 뒤의 모든 숫자를 0으로 만듦.
- release 길이가 부족하면 0을 채워 해당 자리까지 확장함.
- `__replace__(release=...)`를 사용해 새 `Version`을 반환하므로 epoch는 유지되고 pre/post/dev/local은 버려짐.
- 유효하지 않은 `part` 값은 `ValueError`를 던짐.