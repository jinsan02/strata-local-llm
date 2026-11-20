수정 사항을 요약하면:

`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다. 이 메서드는:

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나이면 해당 인덱스의 release 요소를 1 증가시키고, 뒤의 모든 요소를 0 으로 만든다.
- release 길이가 요청된 인덱스보다 짧으면 0 으로 채워 늘린 후 해당 위치를 1 로 설정한다 (예: `1` → `bump("micro")` → `1.0.1`).
- epoch 는 유지하고, pre/post/dev/local 은 모두 버린다.
- 그 밖의 `part` 값은 `ValueError` 를 던진다.
- 원래 객체는 변경하지 않고 새 `Version` 인스턴스를 반환한다.