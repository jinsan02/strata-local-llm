수정 내용을 요약하면 다음과 같습니다:

1. **`src/packaging/utils.py`** 에서 `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 을 추가했습니다.
2. `from collections.abc import Iterable` 임포트를 추가했습니다.
3. 기존 검사(확장자, 대시 개수, 프로젝트 이름, 버전, 빌드 번호, 태그)가 모두 통과한 후 `platforms is not None` 일 때만 플랫폼 검사를 수행합니다.
4. `platforms` 가 plain `str` 이면 `TypeError` 를 던집니다.
5. 사용자 제공 플랫폼 이름과 Tag 의 platform 을 모두 정규화합니다(`.`·`-`·공백 → `_`, 소문자).
6. 태그 중 하나라도 플랫폼이 `"any"` 이거나 정규화된 플랫폼 목록과 일치하면 통과합니다.
7. 일치하지 않으면 `InvalidWheelFilename` 을 던집니다.
8. 기존 동작 (`platforms=None`) 은 변경되지 않습니다.