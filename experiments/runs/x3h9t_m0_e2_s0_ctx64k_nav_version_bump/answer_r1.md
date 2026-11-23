기존 테스트 전체(51524개)가 통과했습니다. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release의 첫째, 둘째, 셋째 숫자를 1 올리고 뒤의 숫자를 0으로 설정합니다.
- 올릴 자리가 release 길이보다 크면 0을 채워 확장합니다.
- epoch는 유지하고, pre/post/dev/local은 모두 버립니다.
- 그 밖의 `part` 값은 `ValueError`를 던집니다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환합니다.