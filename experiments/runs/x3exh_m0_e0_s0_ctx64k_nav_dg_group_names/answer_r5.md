수정 사항을 요약하면:

1. **`InvalidGroupName` 예외 클래스 추가**: `ValueError` 하위 클래스로 `dependency_groups.py`에 정의.
2. **`__all__` 업데이트**: `"InvalidGroupName"`을 공개 exports에 추가.
3. **`canonicalize_name`/`InvalidName` import**: `utils` 모듈에서 가져와 기존 정규식(`_validate_regex`)을 재사용.
4. **`_normalize_group_names` 수정**: 각 그룹 이름에 `canonicalize_name(..., validate=True)`를 적용해 유효성 검사. 규칙 위반 시 `InvalidGroupName`을 `_ErrorCollector`에 추가해 기존 오류(중복 이름 등)와 같은 방식으로 한꺼번에 보고.
5. **`lookup()` 수정**: 정규화 전에 `canonicalize_name(group, validate=True)`로 즉시 검사, 위반 시 `InvalidGroupName` 단일 예외 던짐.
6. **`resolve()` 수정**:同上.

이름 유효성 검사 메시지는 `InvalidName`이 생성하는 `"name is invalid: {name!r}"` 형태를 그대로 사용하므로 원래 이름이 `repr` 형태로 포함됨. 기존 동작(정규화, 중복 검사, include, 순환 검사)은 변경 없음.