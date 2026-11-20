수정 내용 요약:

- **파일**: `src/packaging/version.py`
- **위치**: `Version` 클래스 내 `micro` 프로퍼티 뒤, `_trim_release` 메서드 앞에 `bump(part: str) -> Version` 메서드 추가

**구현 상세**:
- `"major"`(index 0), `"minor"`(index 1), `"micro"`(index 2) 인자만 허용, 나머지는 `ValueError`
- 해당 위치의 release 숫자를 +1 하고 뒤쪽 모든 요소를 0으로 설정
- 올릴 자리가 현재 release 길이보다 크면 0을 채워 튜플 확장 (예: `1` → micro → `(1,0,1)`)
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 `None`으로 버림
- `self.__replace__()`를 사용해 새 `Version` 객체 반환 (원본 불변)