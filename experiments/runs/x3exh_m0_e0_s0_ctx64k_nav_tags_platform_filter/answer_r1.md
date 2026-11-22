수정 내용 요약:

1. **`src/packaging/utils.py`**:
   - `collections.abc.Iterable` import 추가
   - `tags._normalize_string` import 추가
   - `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `str`인 경우 `TypeError` 던짐
   - 기존 파일명 검사(확장자, 대시 개수, 이름, 버전, 빌드 번호, 태그) 후, `platforms`가 `None`이 아니면 각 플랫폼 이름을 `_normalize_string(p).lower()`로 정규화하여 비교. 태그 중 하나라도 `platform == "any"`이거나 정규화된 플랫폼 이름과 일치하면 통과, 아니면 `InvalidWheelFilename` 던짐
   - docstring에 `platforms` 파라미터 설명 및 `.. versionadded:: 26.4` 추가