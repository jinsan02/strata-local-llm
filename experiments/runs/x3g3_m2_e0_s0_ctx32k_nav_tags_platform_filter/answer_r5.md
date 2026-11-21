`src/packaging/utils.py` 파일에서 다음을 수정했습니다:

1. `from collections.abc import Iterable` import 추가
2. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
3. 함수 본문에 `platforms` 검증 로직 추가:
   - `platforms`가 `str`이면 `TypeError` 던짐
   - 각 플랫폼 이름을 `.`, `-`, 공백을 `_`로 바꾸고 소문자로 정규화
   - 태그 중 `platform == "any"`인 것이 있거나 정규화한 플랫폼 이름 중 하나와 일치하는 것이 있으면 통과
   - 일치하는 것이 없으면 `InvalidWheelFilename` 던짐
4. docstring에 `platforms` 파라미터 설명과 `:raises TypeError`, `.. versionadded:: 26.4` 추가