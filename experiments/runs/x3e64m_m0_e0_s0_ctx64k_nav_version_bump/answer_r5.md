수정 내용:

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다. 메서드는 `micro` property 뒤, `_trim_release` 앞에 위치합니다.

구현 요점:
- `part`가 `"major"`/`"minor"`/`"micro"`에 따라 release 튜플의 해당 인덱스(0/1/2)를 1 증가시키고, 뒤의 모든 요소를 0으로 설정
- release 길이가 부족하면 0을 채워 확장
- `__replace__`를 호출해 새 `Version` 객체 반환 (원본 불변)
- epoch는 그대로 유지, pre/post/dev/local은 모두 None으로 버림
- 유효하지 않은 `part` 값은 `ValueError` 던짐