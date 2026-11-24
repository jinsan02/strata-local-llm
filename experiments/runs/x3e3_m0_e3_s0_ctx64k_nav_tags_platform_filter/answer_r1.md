수정 완료. `src/packaging/utils.py` 파일에 다음 사항을 적용했습니다:

1. `from collections.abc import Iterable` import 추가
2. 플랫폼 이름 정규화(`.`/`-`/공백 → `_`, 소문자) 및 매칭 로직을 담당하는 `_normalize_platform`, `_platforms_match` 헬퍼 함수 추가
3. `parse_wheel_filename` 함수 시그니처에 키워드 전용 `platforms: Iterable[str] | None = None` 파라미터 추가
4. 검증 로직 구현: `platforms`가 `str`이면 `TypeError`, 정규화 후 매칭되지 않으면 `InvalidWheelFilename` 던짐. `any` 플랫폼 태그는 빈 iterable 포함 모든 경우 통과
5. docstring 및 `.. versionadded:: 26.4` 문서화 업데이트

기존 동작과 테스트 파일은 수정하지 않았습니다.