수정 완료. 변경 사항을 요약하면:

1. **`InvalidGroupName` 예외 클래스 추가** (`ValueError` 하위 클래스) — 그룹 이름이 core metadata `Name` 규칙을 따르지 않을 때 사용.
2. **`__all__` 에 `"InvalidGroupName"` 추가** — 공개 API로 노출.
3. **`from . import utils` import 추가** — `utils.canonicalize_name(..., validate=True)`와 `utils.InvalidName`를 사용.
4. **`_normalize_group_names()` 수정** — 각 그룹 이름에 `utils.canonicalize_name(group_name, validate=True)`를 호출해 유효성 검사. 실패 시 `InvalidGroupName`을 `_ErrorCollector`에 추가해 기존 오류(중복 이름 등)와 같은 방식으로 한꺼번에 보고.
5. **`DependencyGroupResolver.lookup()` 수정** — 정규화 전에 `utils.canonicalize_name(..., validate=True)`로 검사, 실패 시 `InvalidGroupName`을 즉시 던짐.
6. **`DependencyGroupResolver.resolve()` 수정** —同上, 정규화 전에 유효성 검사 후 실패 시 `InvalidGroupName` 즉시 던짐.