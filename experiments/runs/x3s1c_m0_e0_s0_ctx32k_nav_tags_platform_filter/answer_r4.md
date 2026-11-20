수정을 완료했다. 변경 사항을 요약하면:

1. **`from collections.abc import Iterable`** import 추가
2. **`parse_wheel_filename` 함수 시그니처**에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
3. **플랫폼 검증 로직** 추가:
   - `platforms`가 `None`이면 기존 동작 유지
   - `platforms`가 `str`이면 `TypeError` 던짐
   - 그렇지 않으면 각 플랫폼 이름을 `.`·`-`·공백 → `_` 치환 + 소문자로 정규화하고, wheel 태그 중 하나라도 정규화된 플랫폼 이름과 일치하거나 `"any"`이면 통과, 아니면 `InvalidWheelFilename` 던짐
4. **docstring**에 `platforms` 파라미터 설명과 `.. versionadded:: 26.4` 주석 추가