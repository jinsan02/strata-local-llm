수정 내용을 요약하면:

1. **`src/packaging/utils.py`** 파일 수정:
   - `from collections.abc import Iterable` import 추가
   - `_normalize_platform(platform: str) -> str` 헬퍼 함수 추가: `.`, `-`, 공백을 `_` 로 바꾸고 소문자로 변환 (packaging.tags 의 규칙과 동일)
   - `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
   - `platforms` 가 `None` 이 아니면:
     - `str` 을 직접 주면 `TypeError` 던짐
     - iterable 의 각 원소를 `_normalize_platform` 로 정규화하여 집합으로 저장
     - wheel 태그의 플랫폼 중 `"any"`이거나 정규화된 플랫폼 집합에 포함되면 통과, 아니면 `InvalidWheelFilename` 던짐
   - docstring 에 `platforms` 파라미터 설명 추가