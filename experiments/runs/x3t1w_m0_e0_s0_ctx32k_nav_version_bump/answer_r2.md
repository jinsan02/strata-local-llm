수정 사항을 요약하면 다음과 같다.

**파일**: `src/packaging/version.py`  
**변경**: `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다 (약 50 줄).

메서드 동작:
- `"major"`, `"minor"`, `"micro"` 인자 각각에 대해 release 튜플의 해당 위치(inx=0,1,2) 숫자를 1 증가시킨다.
- 증가한 위치 뒤의 기존 요소들은 모두 0 으로 만든다 (release 길이 유지).
- 증가할 자리가 기존 release 에 없으면 0 을 채워 해당 인덱스까지 늘린다 (`1` → micro → `1.0.1`).
- pre/post/dev/local 세그먼트는 모두 버린다. epoch 는 그대로 유지된다.
- 잘못된 `part` 값은 `ValueError` 를 던진다.
- 기존 객체는 변경하지 않고 새 `Version` 을 반환한다 (`__replace__` 사용).