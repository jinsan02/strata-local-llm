### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
      def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
          """
          Lookup a group name, returning the parsed dependency data for that group.
          This will not resolve includes.

          :param group: the name of the group to lookup
          """
          group = _normalize_name(group)
=======
      def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
          """
          Lookup a group name, returning the parsed dependency data for that group.
          This will not resolve includes.

          :param group: the name of the group to lookup
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"invalid group name {group!r}")
          group = _normalize_name(group)
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
      def resolve(self, group: str) -> tuple[Requirement, ...]:
          """
          Resolve a dependency group to a list of requirements.

          :param group: the name of the group to resolve
          """
          group = _normalize_name(group)
=======
      def resolve(self, group: str) -> tuple[Requirement, ...]:
          """
          Resolve a dependency group to a list of requirements.

          :param group: the name of the group to resolve
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"invalid group name {group!r}")
          group = _normalize_name(group)
>>>>>>> REPLACE

---

`lookup()`와 `resolve()` 메서드에 진입 즉시 그룹 이름 유효성 검사를 추가하여, 정규화 전에 규칙을 위반한 이름을 넘기면 `InvalidGroupName` 예외를 단일 예외로 던지도록 수정했습니다. 이전에 이미 추가했던 `InvalidGroupName` 클래스 정의, `__all__` 등록, `_validate_regex` import, 그리고 `__init__` 내에서의 일괄 검증 로직과 함께 작업이 완료되었습니다. 기존 테스트 파일은 변경하지 않았습니다.