수정 내용을 요약하면:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `collections.abc.Iterable` import 추가
   - `platforms`가 `None`이 아니면:
     - `str`을 직접 주면 `TypeError` 던짐
     - 제공된 플랫폼 이름들을 정규화(`.`·`-`·` ` → `_`, 소문자)하여 `frozenset`으로 저장
     - 태그들의 플랫폼 중 `any`가 있으면 무조건 통과
     - 정규화된 태그 플랫폼이 정규화된 요청 플랫폼 집합과 교차하면 통과
     - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 던짐
   - 기존 동작(`platforms=None`)은 변경 없음
   - docstring에 `platforms` 파라미터 설명 및 `.. versionadded:: 26.4` 추가