`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나일 때 해당 인덱스의 release 숫자를 1 올리고, 뒤의 숫자들은 0으로 설정한다.
- 올릴 자리가 release 튜플에 없으면 0을 채워 해당 길이까지 늘린다.
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버린다.
- 잘못된 `part` 값에 대해 `ValueError`를 던진다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.

기존 테스트 51524개 모두 통과함.