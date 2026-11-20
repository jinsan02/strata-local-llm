`packaging.utils.parse_wheel_filename` 함수에 `platforms` 키워드 전용 인자를 추가했습니다.

**변경 사항 (`src/packaging/utils.py`)**:
1. `collections.abc.Iterable` 임포트 추가.
2. `_normalize_string` 유틸리티 함수 임포트 추가.
3. `parse_wheel_filename` 시그니처에 `platforms: Iterable[str] | None = None` 파라미터 추가.
4. `platforms` 인자에 대한 설명이 포함된 docstring 업데이트.
5. 반환 전에 플랫폼 필터링 로직 구현:
   - `None`이 아니면 입력값이 문자열(`str`)인지 확인하여 오류 처리 (`TypeError`).
   - 사용자 제공 플랫폼 이름을 `_normalize_string` 규칙과 소문자 변환으로 정규화하여 집합 생성.
   - wheel 태그의 플랫폼 이름 중 하나라도 `any`이거나 정규화된 플랫폼 이름 집합과 일치하면 통과, 아니면 `InvalidWheelFilename` 발생.