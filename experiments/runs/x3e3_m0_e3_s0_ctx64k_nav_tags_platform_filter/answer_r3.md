src/packaging/utils.py 파일에 다음 사항을 수정했습니다:
1. `collections.abc.Iterable` import 추가.
2. 플랫폼 태그 정규화 헬퍼 함수 `_normalize_platform_tag` 추가 (`.`/`-`/` ` → `_`, 소문자 변환).
3. `parse_wheel_filename` 함수 시그니처에 `platforms` 키워드 전용 인자 추가 (기본값 `None`).
4. `platforms` 인자에 대한 검증 로직 추가: `str` 전달 시 `TypeError`, 정규화 후 매칭 실패 시 `InvalidWheelFilename` 발생. 태그 플랫폼이 `any`이면 항상 통과.
5. 함수 docstring에 새 파라미터 설명 및 버전 정보(`26.4`) 업데이트.

기존 동작 및 반환값은 변경되지 않았습니다.