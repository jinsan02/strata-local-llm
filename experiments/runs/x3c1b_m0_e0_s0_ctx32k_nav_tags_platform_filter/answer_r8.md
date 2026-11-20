`src/packaging/utils.py` 파일의 `parse_wheel_filename` 함수를 다음과 같이 수정했습니다:

1. `collections.abc.Iterable` 임포트 추가 및 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가.
2. 기존 파일명/태그 검증 로직 완료 후, `platforms`가 `None`이 아닌 경우 추가 검증 수행:
   - `str`을 직접 전달하면 `TypeError` 발생.
   - iterable 내 문자열을 tags.py의 정규화 규칙(`.`·`-`·공백 → `_`, 소문자)과 동일하게 변환.
   - 변환된 이름 중 하나라도 태그의 플랫폼과 일치하면 통과, `"any"` 플랫폼을 포함한 경우나 빈 iterable인 경우에도 무조건 통과.
   - 매칭되는 플랫폼이 없으면 `InvalidWheelFilename` 발생.
3. Docstring에 새로운 파라미터 설명 및 `.. versionadded:: 25.0` 문서화 추가.

기존 기본 동작(`platforms=None`)은 완전히 동일하게 유지되었으며, 반환값과 기존 예외 흐름도 변경되지 않았습니다.