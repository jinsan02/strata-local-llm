`src/packaging/utils.py` 파일에 다음 사항을 수정했습니다:

1. `from collections.abc import Iterable` 임포트 추가
2. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
3. docstring에 `platforms` 파라미터 설명 및 `.. versionadded:: 26.4` 주석 추가
4. 반환 전 플랫폼 검증 로직 추가:
   - `platforms`에 단일 문자열이 전달되면 `TypeError` 발생
   - 제공된 플랫폼 목록을 `.`/`-`/공백 → `_` 치환 및 소문자 변환으로 정규화
   - 휠 태그 중 정규화된 플랫폼과 일치하거나 `any`인 것이 없으면 `InvalidWheelFilename` 발생