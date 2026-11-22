수정 내용을 요약하면:

1. **`src/packaging/utils.py`** 에 `collections.abc.Iterable` import 추가
2. **`_normalize_string()`** 헬퍼 함수 추가: `.`, `-`, 공백을 `_` 로 바꾸고 소문자로 정규화 (packaging.tags 의 규칙과 동일)
3. **`parse_wheel_filename()`** 에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
4. 기존 검증이 끝난 후 플랫폼 필터링 로직 추가:
   - `platforms` 가 `str` 이면 `TypeError`
   - wheel 태그 중 `platform == "any"` 가 있으면 무조건 통과 (빈 iterable 포함)
   - 아니면 정규화한 `platforms` 와 wheel 의 platform 태그 간 교집합 검사, 없으면 `InvalidWheelFilename`
5. docstring 에 `platforms` 파라미터 설명과 `.. versionadded:: 26.4` 주석 추가