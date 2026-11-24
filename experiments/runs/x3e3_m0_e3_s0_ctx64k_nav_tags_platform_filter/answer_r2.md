수정을 완료했습니다. 변경 내용을 요약하면:

1. `collections.abc.Iterable` import 추가
2. `_normalize_platform(platform)` 헬퍼 함수 추가: `.`, `-`, 공백을 `_`로 바꾸고 소문자로 변환
3. `parse_wheel_filename` 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
4. docstring에 `platforms` 파라미터 설명 추가
5. 태그 파싱 후 플랫폼 검증 로직 추가:
   - `platforms`가 `str`이면 `TypeError` 던짐
   - `platforms`가 `None`이면 기존 동작 유지
   - 제공된 플랫폼 이름들을 정규화한 집합과 태그의 플랫폼 정규화 집합을 교차 검사
   - 태그 중 `platform == "any"`가 있으면 모든 `platforms`에 통과 (빈 iterable 포함)
   - 매칭되는 플랫폼이 없으면 `InvalidWheelFilename` 던짐