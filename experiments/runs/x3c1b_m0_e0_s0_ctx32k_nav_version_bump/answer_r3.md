src/packaging/version.py 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

이 메서드는 다음과 같은 기능을 수행합니다:
- `part` 값에 따라 release의 해당 위치(`major`=0, `minor`=1, `micro`=2) 값을 1 증가시킵니다.
- 증가된 위치 이후의 모든 release 값을 0으로 초기화합니다.
- 요청한 위치가 기존 release 길이보다 길면 해당 길이까지 0을 채워 늘립니다 (기존 trailing zeros는 유지).
- epoch는 그대로 두며, pre/post/dev/local 세그먼트는 모두 제거합니다.
- 유효하지 않은 `part` 값이 입력되면 `ValueError`를 발생시킵니다.