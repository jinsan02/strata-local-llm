수정 내용:

`src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Self` 메서드를 추가했습니다 (라인 596 근처, `__replace__` 메서드 직후).

메서드는 다음과 같이 동작합니다:
- `"major"`: release[0] 를 1 올리고 뒤의 모든 요소를 0 으로 설정
- `"minor"`: release[1] 를 1 올리고 뒤의 모든 요소를 0 으로 설정  
- `"micro"`: release[2] 를 1 올리고 뒤의 모든 요소를 0 으로 설정
- 올릴 인덱스가 현재 release 길이보다 크면 0 을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch 는 유지, pre/post/dev/local 은 모두 버림
- 유효하지 않은 part 값은 `ValueError` 던짐
- 불변성 보장 (새 Version 객체 반환)