수정을 완료했다. 변경 사항을 요약하면:

1. **`InvalidGroupName` 예외 클래스 추가** (`ValueError` 하위 클래스) — `dependency_groups.py`의 Error Types 섹션에 추가
2. **`__all__`에 `"InvalidGroupName"` 추가**
3. **`_validate_group_name()` 헬퍼 함수 추가** — `packaging.utils.canonicalize_name(name, validate=True)`를 사용해 core metadata Name 규칙 검증. `InvalidName`을 `InvalidGroupName`으로 변환
4. **`_normalize_group_names()` 수정** — 각 그룹 이름에 대해 `_validate_group_name()`을 호출하고 `InvalidGroupName`을 기존 오류 수집기(`_ErrorCollector`)에 추가. 중복 이름 등 기존 오류와 같은 방식으로 한꺼번에 보고
5. **`lookup()` 수정** — 정규화 전에 `_validate_group_name(group)` 호출. 규칙 위반 시 단일 `InvalidGroupName` 예외를 바로 던짐
6. **`resolve()` 수정** — 정규화 전에 `_validate_group_name(group)` 호출. 규칙 위반 시 단일 `InvalidGroupName` 예외를 바로 던짐
7. **`from .utils import InvalidName, canonicalize_name` import 추가**

기존 동작(정규화, 중복 검사, include, 순환 검사)은 모두 변경되지 않았다.