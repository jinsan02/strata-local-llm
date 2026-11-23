수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`**
   - `from collections.abc import Iterable` import 추가
   - `_normalize_platform(platform: str) -> str` 헬퍼 함수 추가: `.replace(".", "_").replace("-", "_").replace(" ", "_").lower()` 수행 (packaging.tags의 `_normalize_string`과 동일한 규칙)
   - `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
   - 기존 파일명 검사(확장자, 대시 수, 이름, 버전, 빌드 번호, 태그)가 끝난 후 `platforms` 검증을 추가:
     - `platforms`가 `str`이면 `TypeError` 던짐
     - `platforms`가 `None`이 아니면 각 플랫폼 태그를 `_normalize_platform`로 정규화하여 제공된 이름 집합과 비교
     - 태그 중 하나라도 `platform == "any"`이거나 정규화된 이름이 제공된 플랫폼 집합에 있으면 통과
     - 모두 일치하지 않으면 `InvalidWheelFilename` 던짐
   - docstring에 `platforms` 파라미터 설명 및 `.. versionadded:: 26.4` 추가