수정을 완료했습니다. `src/packaging/utils.py` 파일에 다음 사항을 적용했습니다:

1. `_normalize_platform(platform)` 헬퍼 함수 추가: `.`, `-`, 공백을 `_`로 변환하고 소문자로 내립니다.
2. `parse_wheel_filename()` 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가.
3. `platforms`에 빈 문자열이 아닌 `str` 타입이 직접 전달되면 즉시 `TypeError`를 발생시키는 검사 추가.
4. 기존 파싱 검증(`filename`, `dashes`, `name`, `version`, `build`, `tag parsing`)이 모두 완료된 후, 플랫폼 필터링 로직 구현: 제공된 플랫폼 목록과 정규화된 태그가 일치하거나 태그의 플랫폼이 `"any"`이면 통과, 아니면 `InvalidWheelFilename` 발생.
5. `collections.abc.Iterable` import 및 함수 docstring 업데이트.

기존 동작은 완전히 유지되며, 새로운 인자는 필요할 때만 동작합니다. 작업 종료.