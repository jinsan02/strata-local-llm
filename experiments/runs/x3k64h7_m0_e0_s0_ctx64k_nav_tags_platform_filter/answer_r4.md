수정을 마쳤습니다. `src/packaging/utils.py` 파일에 다음 사항을 적용했습니다:

1. `collections.abc.Iterable` import 추가
2. `_normalize_platform()` 헬퍼 함수 추가 (`.`, `-`, 공백을 `_`로 치환 후 소문자화)
3. `parse_wheel_filename` 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
4. `platforms` 검증 로직 추가: `str` 입력 시 `TypeError`, 정규화 후 매칭 실패 시 `InvalidWheelFilename` 발생
5. docstring 업데이트

기존 동작 및 반환값은 모두 유지됩니다.