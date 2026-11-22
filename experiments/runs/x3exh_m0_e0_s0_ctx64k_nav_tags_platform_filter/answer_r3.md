수정 완료. 변경 내용 요약:

1. **`src/packaging/utils.py`**:
   - `Iterable` 타입과 `_normalize_string` 함수 import 추가
   - `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - docstring에 `platforms` 파라미터 설명 및 `.. versionadded:: 26.4` 주석 추가
   - 기존 파일명 검사(확장자, dash 개수, 이름, 버전, 빌드번호, 태그)가 완료된 후 `platforms` 검증 로직 추가:
     - `platforms`가 `str`이면 `TypeError` 발생
     - `_normalize_string(p).lower()`로 정규화하여 `frozenset`으로 저장
     - 태그 중 `platform == "any"`가 있으면 항상 통과
     - `"any"`가 없고 정규화된 플랫폼 집합과 교집합이 없으면 `InvalidWheelFilename` 발생
   - 반환값은 기존과 동일하게 `(name, version, build, tags)` 튜플 반환