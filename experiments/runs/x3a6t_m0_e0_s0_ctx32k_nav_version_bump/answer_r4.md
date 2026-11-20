`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

구현 내용:
- `"major"`, `"minor"`, `"micro"` 세 가지 part를 지원하며, 각각 release 튜플의 첫 번째, 두 번째, 세 번째 숫자를 1 올립니다.
- 올린 위치 이후의 모든 release 숫자는 0으로 초기화합니다.
- release 길이가 target index보다 짧으면 0을 채워 늘립니다 (예: `1` → micro → `1.0.1`).
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 제거됩니다.
- 잘못된 part 값이 들어오면 `ValueError`를 던집니다.
- 원래 객체는 불변이며 새 `Version` 인스턴스를 반환합니다.

기존 테스트 51524개 모두 통과 확인했습니다.