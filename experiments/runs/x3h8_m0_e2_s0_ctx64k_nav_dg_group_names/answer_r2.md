### 요구사항 확인 결과

1. **core metadata `Name` 규칙 사용 (새 정규식 금지)**
   - `src/packaging/dependency_groups.py:17` — `from .utils import _validate_regex`로 기존 구현 재사용
   - `src/packaging/dependency_groups.py:340`, `157`, `172` — 검증에 `_validate_regex.fullmatch()` 사용

2. **`InvalidGroupName` 추가 및 `__all__` 등록**
   - `src/packaging/dependency_groups.py:47-52` — `class InvalidGroupName(ValueError)` 정의
   - `src/packaging/dependency_groups.py:25` — `__all__`에 `"InvalidGroupName"` 포함

3. **`DependencyGroupResolver.__init__`에서 한꺼번에 보고**
   - `src/packaging/dependency_groups.py:332-355` — `_normalize_group_names`에서 그룹 키마다 검증, 실패 시 `errors.error(InvalidGroupName(...))`로 수집
   - `src/packaging/dependency_groups.py:137-148` — `errors.finalize()`로 기존 오류(중복 등)와 함께 일괄 보고
   - 메시지 포맷: `f"{group_name!r} is not a valid dependency group name"` (원래 이름 `repr` 포함)

4. **`lookup()`/`resolve()`에서 단일 예외 즉시 던지기**
   - `src/packaging/dependency_groups.py:157-158` — `lookup()`에서 정규화 전 검증, 실패 시 즉시 `raise InvalidGroupName(...)`
   - `src/packaging/dependency_groups.py:172-173` — `resolve()`에서 정규화 전 검증, 실패 시 즉시 `raise InvalidGroupName(...)`

5. **기존 동작 변경 없음**
   - 정규화(`_normalize_name`), 중복 검사(`DuplicateGroupNames`), include/순환 검사(`_validate`, `_resolve`), 파싱(`_parse_group`) 로직 모두 기존 그대로 유지

모든 요구사항 반영 완료. 자동 검사(코드 검사, 테스트 129개 통과)도 성공. 추가 수정 불필요.