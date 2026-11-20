`DependencyGroupResolver.__init__` 에서 `_normalize_group_names` 내의 유효성 검사 예외가 바로 상위 호출로 전파되면, `_ErrorCollector.finalize()` 가 예외 목록을 수집하지 못해 다른 오류(중복 이름 등)와 함께 `ExceptionGroup` 으로 한꺼번에 보고되지 않습니다. 따라서 검증 예외를 포착하여 `errors` 컬렉터에 추가하도록 수정했습니다.

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    for group_name, value in dependency_groups.items():
        _validate_name(group_name)
        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value
=======
    for group_name, value in dependency_groups.items():
        try:
            _validate_name(group_name)
        except InvalidGroupName as e:
            errors.error(e)
            continue
        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value
>>>>>>> REPLACE

`lookup()`과 `resolve()` 의 초기 검증, `InvalidGroupName` 정의 및 `__all__` 등록, 유틸리티 `_validate_regex` 사용은 이전 편집에서 이미 완료되었습니다. 나머지 변경사항 없이 기존 동작을 유지합니다.