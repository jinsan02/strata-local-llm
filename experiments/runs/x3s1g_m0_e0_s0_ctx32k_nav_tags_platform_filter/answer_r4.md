### 요약

다음 내용을 수정함:

**1. `src/packaging/utils.py`**
- `_normalize_platform(platform: str) -> str` 함수 추가: `.`, `-`, 공백을 `_`로 바꾸고 소문자로 변환.
- `parse_wheel_filename` 시그니처에 `*, platforms: Iterable[str] | None = None` 키워드 전용 인자 추가.
- 기존 검사(확장자, 이름, 버전, 빌드 번호, 태그) 통과 후 `platforms is not None`일 때만 검증 수행.
    - `isinstance(platforms, str)`이면 `TypeError`.
    - 입력 iterable의 모든 원소를 `_normalize_platform`로 정규화한 집합을 만듦.
    - 휠의 `Tag.platform`이 `"any"`이거나 정규화된 집합에 포함되면 통과(`matched = True`).
    - 아무 태그도 조건을 만족하지 않으면 `InvalidWheelFilename` 발생.
- `platforms=None`(기본값)이면 기존과 동일하게 플랫폼 검증을 건너뛰고 반환.
- `from collections.abc import Iterable` import 추가.