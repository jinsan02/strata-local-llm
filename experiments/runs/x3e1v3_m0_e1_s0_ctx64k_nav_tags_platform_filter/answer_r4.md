수정 내용 요약:
- `src/packaging/utils.py`에 `from collections.abc import Iterable` import 추가
- `_normalize_platform(platform: str) -> str` 헬퍼 함수 추가 (`.`, `-`, ` `를 `_`로 치환 후 소문자화)
- `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
- `platforms` 필터링 로직 추가:
  - `platforms`가 `str`이면 `TypeError` 발생
  - `None`이 아니면 제공된 플랫폼 이름들을 정규화하여 집합으로 만듦
  - 태그 중 플랫폼이 `any`이거나 정규화된 플랫폼 집합에 포함되면 통과, 아니면 `InvalidWheelFilename` 발생
- 함수 docstring에 `platforms` 파라미터 설명 및 버전 정보 추가