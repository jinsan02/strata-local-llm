수정 사항을 요약하면:

1. **`src/packaging/utils.py`** — `collections.abc.Iterable` import 추가
2. **`_normalize_platform()`** 헬퍼 함수 추가: `.`, `-`, 공백을 `_`로 바꾸고 소문자로 정규화 (tags 모듈과 동일한 규칙)
3. **`parse_wheel_filename()`** 시그니처에 키워드 전용 `platforms: Iterable[str] | None = None` 파라미터 추가
4. `platforms`가 `None`이 아니면:
   - `str`을 주면 `TypeError` 발생
   - 모든 플랫폼 이름을 정규화한 후 `frozenset`으로 저장
   - 태그 중 하나라도 `platform == "any"`이거나 정규화된 태그가 `normalized_platforms`에 있으면 통과
   - 없으면 `InvalidWheelFilename` 발생
5. docstring에 새 파라미터 설명 및 버전 정보 추가