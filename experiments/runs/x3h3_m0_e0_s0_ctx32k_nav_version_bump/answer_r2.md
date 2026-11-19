`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다. 

- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError`를 던집니다.
- 해당 인덱스의 release 값을 1 올리고, 뒤의 값들은 모두 0으로 만듭니다.
- release 길이가 부족한 경우 0으로 채워 늘립니다.
- epoch는 유지하고, pre/post/dev/local은 모두 제거된 새 `Version` 객체를 반환합니다.