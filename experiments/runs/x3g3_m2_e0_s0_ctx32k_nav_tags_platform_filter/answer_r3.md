수정 사항을 요약하면:

1. **`src/packaging/utils.py`**:
   - `from collections.abc import Iterable` import 추가
   - `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `None`이 아니면:
     - `platforms`가 `str`이면 `TypeError` 던짐
     - 각 플랫폼 이름을 `.`·`-`·공백 → `_` 치환 + 소문자로 정규화
     - 태그 중 하나라도 정규화한 이름과 일치하거나 `any`이면 통과, 아니면 `InvalidWheelFilename` 던짐
   - 기존 검사(확장자, 이름, 버전, 빌드번호, 태그)는 `platforms` 체크 전에 실행되어 기존 오류 메시지 유지
   - 반환값은 기존과 동일 (`frozenset[Tag]` 거름 없음)
   - `_normalize_platform_name(name)` 헬퍼 함수 추가 (정규화 로직)
   - docstring에 `platforms` 파라미터 문서화 및 버전 정보 추가