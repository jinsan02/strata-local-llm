수정을 완료했다.

### 변경 사항 요약
`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다:
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나이면 해당 인덱스의 release 숫자를 1 올리고 뒤쪽 모두를 0으로 만든다.
-release 길이가 짧아도 0을 채워 필요한 자리까지 늘린다.
- `__replace__(release=..., pre=None, post=None, dev=None, local=None)`로 새 Version을 반환하므로 epoch는 그대로 유지되고 pre/post/dev/local은 버려진다.
- 유효하지 않은 part 값은 `ValueError`를 던진다.