수정 완료. 변경 사항을 요약하면:

1. `typing.Iterable` 임포트 추가
2. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
3. `platforms`가 `None`이 아닌 경우:
   - `str`을 직접 주면 `TypeError` 던짐
   - 각 플랫폼 이름을 `.`·`-`·` ` → `_`로 바꾸고 소문자로 정규화하여 비교용 집합 구성
   - 태그 중 하나라도 플랫폼이 `"any"`이거나 정규화한 이름이 집합에 있으면 통과, 아니면 `InvalidWheelFilename` 던짐
4. 기존 동작 (`platforms=None`) 은 변경 없음
5. docstring 에 `platforms` 파라미터 설명과 `:raises TypeError` 추가, 버전 주석 (`.. versionadded:: 26.5`) 추가