수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

**변경 내용:**
- `micro` property 뒤, `_trim_release` 메서드 앞에 `bump` 메서드 추가 (약 64줄)
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 발생
- 해당 인덱스의 release 숫자를 1 증가시키고, 뒤의 모든 숫자를 0으로 설정
- 인덱스가 현재 release 길이보다 크면 0을 채워 확장
- epoch는 그대로 유지, pre/post/dev/local은 모두 버림
- `__replace__`를 사용해 새 `Version` 객체 반환 (원본 불변)