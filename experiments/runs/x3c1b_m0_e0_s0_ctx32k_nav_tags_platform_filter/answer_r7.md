수정 사항을 요약하면:

1. **`src/packaging/utils.py`**:
   - `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `typing.Iterable` import 추가
   - `platforms is not None` 일 때:
     - 인자가 문자열(`str`)이면 `TypeError` 발생
     - 각 플랫폼 이름을 `.replace(".", "_").replace("-", "_").replace(" ", "_").lower()`로 정규화 (packaging.tags._normalize_string 규칙 동일 + 소문자)
     - wheel의 platform 태그 중 `"any"`가 있으면 항상 통과 (빈 iterable 포함)
     - `"any"`가 없고, 정규화된 platforms 세트와 wheel 플랫폼 태그 간 교집합이 없거나 platforms가 비어 있으면 `InvalidWheelFilename` 발생
   - 기존 검증(확장자, 대시 수, 이름, 버전, 빌드 번호, 태그 파싱)은 그대로 우선 실행
   - 통과 시 반환값은 기존과 동일 (`frozenset[Tag]` 거르지 않음)