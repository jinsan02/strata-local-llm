`src/packaging/utils.py` 파일에 다음 사항을 수정했습니다:

1. `collections.abc` import 추가
2. `.`, `-`, 공백을 `_`로 바꾸고 소문자로 변환하는 `_normalize_platform()` 헬퍼 함수 추가
3. `parse_wheel_filename` 시그니처에 `platforms: collections.abc.Iterable[str] | None = None` 키워드 전용 인자 추가
4. 기존 파일명 검사(`tag_str` 파싱) 완료 후, `platforms is not None`일 때 검증 로직 삽입:
   - 인자가 `str`이면 `TypeError` 던짐
   - 입력 iterable의 플랫폼을 `_normalize_platform`로 정규화한 후 집합으로 변환
   - 휠 태그(`Tag.platform`) 가운데 하나라도 정규화 플랫폼 집합과 일치하거나, 어떤 태그든 `any`를 가지면 통과
   - 조건 불만족 시 기존과 같은 방식으로 `InvalidWheelFilename` 던짐
5. docstring에 `.. versionadded:: 26.5` 및 파라미터 설명 주석 추가

기존 반환값 구조, 에러 메시지 포맷, 기존 테스트 파일은 수정하지 않았습니다.