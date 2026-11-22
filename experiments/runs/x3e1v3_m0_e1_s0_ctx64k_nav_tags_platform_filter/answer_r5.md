수정을 완료했습니다. `src/packaging/utils.py` 파일에서 다음 사항을 변경했습니다:

1. `collections.abc.Iterable` import 추가
2. `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
3. docstring에 새로운 인자의 역할과 `:raises InvalidWheelFilename` 설명 추가
4. 기존 파일명 검사 이후 `platforms` 검증 로직 추가:
   - `platforms`가 `str` 타입이면 `TypeError` 발생
   - 제공된 플랫폼 문자열을 정규화(`.`/`-`/공백 → `_`, 소문자)하여 `frozenset`으로 변환
   - 휠 태그 집합 내 `platform`이 `any`이거나 정규화된 플랫폼과 일치하는 것이 있으면 통과
   - 일치하는 태그가 없으면 `InvalidWheelFilename` 발생
   - 기본값 `None`일 때는 기존 동작과 동일하게 검증 단계 건너뜀