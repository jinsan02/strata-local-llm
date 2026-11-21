`src/packaging/utils.py` 파일에 다음 내용을 수정·추가했습니다:

1. `collections.abc.Iterable` import 추가.
2. `_normalize_platform` 헬퍼 함수 추가 (`.`, `-`, 공백을 `_`로 바꾸고 소문자화).
3. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가.
4. `platforms`가 `str` 타입으로 전달될 때 `TypeError` 발생 로직 구현.
5. `platforms`가 `None`이 아니면 태그의 플랫폼을 정규화한 집합과 교집합을 확인하고, `any` 플랫폼 태그가 없으면 `InvalidWheelFilename`을 던짐.
6. 기존 `platforms=None`일 때는 플랫폼 검증을 건너뛰어 기존 동작과 완전히 동일하게 동작하도록 조건 분기 처리.
7. docstring에 `platforms` 파라미터 설명, `TypeError` 발생 조건, 버전 정보(`.. versionadded:: 26.4`) 추가.

기존 테스트 파일은 건드리지 않았습니다. 작업 완료.