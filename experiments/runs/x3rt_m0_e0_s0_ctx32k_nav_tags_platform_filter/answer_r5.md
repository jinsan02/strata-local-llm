수정 내용 요약:

- `src/packaging/utils.py`에서 `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None`을 추가함.
- `platforms`가 `None`이 아니면 `str` 인스턴스인지 확인하여 `TypeError`를 던짐.
- 제공된 플랫폼 이름들을 `.`·`-`·공백을 `_`로 바꾸고 소문자로 정규화하여 `frozenset`으로 저장.
- 태그의 플랫폼 중 `any`가 있으면 통과. `any`가 없으면 정규화된 태그 플랫폼과 정규화된 요청 플랫폼의 교집합이 비어있으면 `InvalidWheelFilename`을 던짐.
- 기존 동작(기본값 `None`)은 변경 없음. 모든 기존 테스트 317개 통과.