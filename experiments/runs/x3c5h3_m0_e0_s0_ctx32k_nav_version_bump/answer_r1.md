`src/packaging/version.py` 파일의 `Version` 클래스 내 `__replace__` 메서드 뒤에 `bump(self, part: str) -> Self` 메서드를 추가했습니다.

주요 동작:
- `"major"` (인덱스 0), `"minor"` (인덱스 1), `"micro"` (인덱스 2)만 허용하고 나머지는 `ValueError` 발생
- release tuple에서 해당 인덱스의 정수를 1 증가시키고, 뒤의 모든 요소를 0으로 초기화
- 올릴 인덱스가 현재 release 길이보다 크면 0을 채워 늘림 (예: `(1,)` → micro bump → `(1, 0, 1)`)
- `epoch`는 유지하고, pre/post/dev/local은 모두 제거된 새 `Version` 객체 반환