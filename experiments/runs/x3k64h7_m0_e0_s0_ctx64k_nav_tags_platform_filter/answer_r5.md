수정 사항을 요약하면:

**`src/packaging/utils.py`**

1. `from collections.abc import Iterable` import 추가
2. `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
3. 기존 filename 검사(확장자, dash 수, 이름, 버전, 빌드 번호, 태그 파싱)가 먼저 실행된 후, `platforms is not None`일 때만 플랫폼 검증 수행:
   - `isinstance(platforms, str)` → `TypeError`
   - 각 플랫폼 이름을 `.`·`-`·공백 → `_`, 소문자로 정규화하여 `frozenset`으로 변환
   - 태그 중 하나라도 `platform == "any"`이거나 정규화된 플랫폼 집합에 포함되면 통과, 아니면 `InvalidWheelFilename`
4. docstring에 `platforms` 파라미터 설명과 `:raises TypeError:` 추가, `.. versionadded:: 26.4` 주석 추가

기존 동작( `platforms=None` )은 전혀 변경되지 않음.