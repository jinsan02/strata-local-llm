수정을 완료했다. 변경 사항을 요약하면:

1. **`collections.abc.Iterable` import 추가** — `platforms` 파라미터의 타입 힌트를 위해 필요.

2. **`parse_wheel_filename` 함수 시그니처 변경** — 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가.

3. **`str` 타입 체크** — `platforms`가 `str`이면 `TypeError` 던짐.

4. **플랫폼 검증 로직 추가** — `platforms`가 `None`이 아니면:
   - 각 플랫폼 이름을 `.`, `-`, 공백을 `_`로 바꾸고 소문자로 정규화
   - `any` 플랫폼 태그가 있거나 정규화된 태그 중 하나가 `platforms`와 일치하면 통과
   - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 던짐

5. **docstring 업데이트** — `platforms` 파라미터 설명과 `.. versionadded:: 26.4` 추가.