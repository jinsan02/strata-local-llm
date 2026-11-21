수정 내용을 요약하면:

1. `src/packaging/utils.py`에 `from collections.abc import Iterable` import 추가
2. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
3. docstring에 `platforms` 파라미터 설명 및 `.. versionchanged:: 26.4 Added the platforms parameter.` 추가
4. 기존 파일명 검사(확장자, 대시 수, 이름, 버전, 빌드 번호, 태그)가 끝난 후 `platforms` 검증 로직 추가:
   - `platforms`가 `str`이면 `TypeError` 던짐
   - `platforms`의 각 문자열을 `.`·`-`·공백 → `_` 변환 + 소문자로 정규화
   - wheel 태그의 플랫폼 중 `"any"`가 있거나 정규화된 `platforms`와 일치하는 것이 있으면 통과
   - 일치하는 것이 없으면 `InvalidWheelFilename` 던짐
   - `platforms=None`이면 검증 건너뛰어 기존 동작 유지