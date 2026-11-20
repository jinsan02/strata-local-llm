`src/packaging/utils.py`에서 `parse_wheel_filename` 함수에 `platforms: Iterable[str] | None = None` 키워드 전용 인자를 추가했습니다. 

추가된 로직은 다음과 같습니다:
- `platforms`가 `None`이 아닌 경우, 전달된 값이 `str`이면 즉시 `TypeError`를 던집니다.
- 제공된 플랫폼 iterable의 각 문자열을 `packaging.tags`와 동일한 규칙(`.`/`-`/공백 → `_`, 소문자 변환)으로 정규화하여 집합으로 저장합니다.
- 파싱된 태그 집합(`tags`)을 순회하며, 태그의 플랫폼이 `"any"`이거나 정규화된 태그 플랫폼이 `norm_platforms`에 포함되면 통과(`matched = True`)합니다.
- 모든 태그를 확인한 후에도 통과하지 못하면 `InvalidWheelFilename`을 던집니다.
- `platforms=None`일 때는 해당 검증 블록이 실행되지 않아 기존 동작과 완전히 동일하게 유지됩니다.