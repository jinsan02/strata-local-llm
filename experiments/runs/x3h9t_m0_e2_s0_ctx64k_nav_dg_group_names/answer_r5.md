기존 테스트 129개 모두 통과했습니다.

변경 사항 요약:

1. **`InvalidGroupName` 예외 클래스 추가** (`ValueError` 하위 클래스) — `dependency_groups.py`
2. **`__all__`에 `InvalidGroupName` 추가**
3. **`.utils._validate_regex` import** — core metadata `Name` 필드 검증에 쓰이는 기존 정규식 재사용
4. **`_normalize_group_names()` 수정** — 그룹 이름 키마다 `_validate_regex.fullmatch()` 검사. 실패 시 `InvalidGroupName`을 `_ErrorCollector`에 수집 (중복 이름 등 기존 오류와 같은 방식으로 `ExceptionGroup`으로 한꺼번에 보고)
5. **`_validate_group_name()` 헬퍼 함수 추가** — 단일 이름 검증을 위해 사용
6. **`lookup()`과 `resolve()` 수정** — 정규화 전에 `_validate_group_name()` 호출. 규칙 위반 시 `InvalidGroupName`을 즉시 단일 예외로 던짐