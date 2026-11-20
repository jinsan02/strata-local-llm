`src/packaging/utils.py` 파일에 다음 사항을 수정했습니다:

1. `collections.abc.Iterable` 임포트 추가
2. 플랫폼 이름 정규화 헬퍼 함수 `_normalize_platform_tag(platform: str) -> str` 추가 (`.`, `-`, ` ` → `_` 치환 후 소문자화)
3. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
4. `platforms` 검증 로직 추가:
   - `None`이 아니면 `isinstance(platforms, str)` 체크 후 `TypeError` 발생
   - 제공된 iterable을 정규화하여 `frozenset`으로 변환
   - 휠 태그 중 하나라도 `platform == "any"`이거나 정규화된 플랫폼 목록과 매칭되면 통과, 아니면 `InvalidWheelFilename` 발생
5. 함수 docstring에 `platforms` 파라미터 설명 및 버전 정보(`.. versionadded:: 26.4`) 추가

기존 테스트 파일은 수정하지 않았으며, `platforms=None`일 때 기존 동작은 완전히 유지됩니다.