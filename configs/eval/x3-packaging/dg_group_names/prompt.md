packaging 의 dependency group(PEP 735) 처리에 그룹 이름 검사를 추가하라.

- 그룹 이름은 core metadata 의 `Name` 필드와 같은 규칙을 따라야 한다. 이 규칙은 packaging 안에 이미 구현되어 있다. 새 정규식을 만들지 말고 그 구현을 사용하라.
- `packaging.dependency_groups` 에 공개 예외 `InvalidGroupName` (`ValueError` 의 하위 클래스)을 추가하고 `__all__` 에 넣어라.
- `DependencyGroupResolver(...)` 를 만들 때, 규칙에 맞지 않는 그룹 이름(키)마다 `InvalidGroupName` 을 하나씩 만들어 기존 오류(중복 이름 등)와 **같은 방식으로 한꺼번에** 보고하라. 메시지에는 원래 이름이 `repr` 형태로 들어가야 한다.
- `lookup()` 과 `resolve()` 에 규칙에 맞지 않는 이름을 넘기면, 다른 처리 전에 `InvalidGroupName` 을 **단일 예외로** 바로 던져라.
- 규칙에 맞는 이름의 기존 동작(정규화, 중복 검사, include, 순환 검사)은 바뀌면 안 된다.
