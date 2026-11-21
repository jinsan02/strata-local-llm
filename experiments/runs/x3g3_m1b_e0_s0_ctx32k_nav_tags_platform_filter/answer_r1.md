`src/packaging/utils.py` 파일에 다음 사항을 수정했습니다:

1. `collections.abc.Iterable` import 추가
2. `_normalize_platform(platform: str) -> str` 헬퍼 함수 추가 (`.` `- ` ` ` → `_` 치환 및 소문자 변환)
3. `parse_wheel_filename` 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
4. `platforms`가 `str`인 경우 `TypeError` 던지는 검증 로직 추가
5. `platforms`가 `None`이 아닐 때, 태그의 플랫폼이 정규화된 `platforms` 집합과 일치하거나 `any`인 경우만 통과하도록 검증 로직 추가 (불일치 시 `InvalidWheelFilename` 던짐)
6. docstring에 `platforms` 파라미터 설명 및 버전 정보(`26.4`) 추가
7. 기존 `platforms=None` 동작은 완전히 유지됨