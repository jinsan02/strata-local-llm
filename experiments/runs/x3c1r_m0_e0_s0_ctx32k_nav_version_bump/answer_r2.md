`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다. 

요구사항을 모두 반영하였습니다:
- `major`, `minor`, `micro`만 허용하며, 나머지 입력(대소문자 포함)은 `ValueError`를 던집니다.
- 지정한 release 인덱스를 1 증가시키고, 해당 인덱스 뒤의 모든 값을 0으로 초기화합니다.
- release 튜플의 길이가 요청된 인덱스보다 짧으면 자동으로 `0`을 채워 확장합니다.
- epoch는 그대로 유지하고, pre/post/dev/local 세그먼트는 모두 제거합니다.
- 기존 객체를 수정하지 않고 새 `Version` 인스턴스를 반환하며, `__replace__`를 활용하여 캐시 일관성을 보장합니다.