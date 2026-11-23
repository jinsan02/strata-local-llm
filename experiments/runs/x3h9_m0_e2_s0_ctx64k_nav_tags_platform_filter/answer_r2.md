수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`**:
   - `from collections.abc import Iterable` 추가
   - `.tags` 에서 `_normalize_string` 함수 추가 import
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms` 가 `str` 인 경우 `TypeError` 던짐
   - 기존 파일명 검사(확장자, 대시 수, 이름, 버전, 빌드 번호, 태그) 후 `platforms` 가 `None` 이 아니면 플랫폼 태그 매칭 검증
   - 플랫폼 이름은 `_normalize_string(p).lower()` 로 정규화 후 비교 (`.`, `-`, ` ` → `_`, 소문자)
   - 태그 중 `platform == "any"` 인 것이 있으면 항상 통과
   - 매칭되는 플랫폼이 없으면 `InvalidWheelFilename` 던짐
   - 반환값은 기존과 동일 (`frozenset[Tag]` 포함)