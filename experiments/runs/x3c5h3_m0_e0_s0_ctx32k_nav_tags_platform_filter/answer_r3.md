수정 내용 요약:
- `src/packaging/utils.py`의 `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None`를 추가했습니다.
- 기존 동작은 유지하며, `platforms`가 `None`이 아닌 경우에만 검증 로직을 실행합니다.
- `platforms`가 문자열(`str`)인 경우 `TypeError`를 발생시킵니다.
- 제공된 플랫폼 이름과 파일명 내 태그의 플랫폼 이름을 정규화하여 비교합니다. 정규화는 `.`, `-`, 공백을 `_`로 바꾸고 소문자로 변환하는 규칙을 따릅니다.
- 태그 중 플랫폼이 `'any'`인 것이 있거나, 정규화된 태그 이름이 `platforms` 집합에 포함되면 통과합니다.
- 조건을 만족하지 않으면 `InvalidWheelFilename` 예외를 발생시킵니다.