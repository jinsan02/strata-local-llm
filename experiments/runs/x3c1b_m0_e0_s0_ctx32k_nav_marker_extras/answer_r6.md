src/packaging/markers.py, src/packaging/requirements.py 파일에 메서드와 속성을 추가했습니다.
`referenced_extras()`는 마커 트리를 순회하며 `extra`나 `extras` 변수가 쓰인 비교 식에서 문자열 리터럴 값을 추출해 정규화된 이름 집합으로 반환합니다.
`marker_extras`는 해당 메서드를 호출하는 간단한 프로퍼티입니다.

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def evaluate_prepared(
        self, environment: Mapping[str, str | AbstractSet[str]]
    ) -> bool:
=======
      def referenced_extras(self) -> frozenset[str]:
          """Return all extra names referenced in the marker as a sorted set.
  
          Scans every comparison in the marker tree for uses of the ``extra`` variable (e.g. ``extra == "foo"``, ``"foo" in extras``, etc.) and returns the canonicalised extra names found, regardless of whether they are actually selected in the current environment.
  
          >>> from packaging.markers import Marker
          >>> Marker('extra == "Fancy"').referenced_extras()
          frozenset({'fancy'})
          >>> Marker(
          ...     'extra == "Foo" or extra == "Bar"'
          ... ).referenced_extras()
          frozenset({'bar', 'foo'})
  
          .. versionadded:: 26.5
          """
          return _collect_extra_names(self._markers)

      def evaluate_prepared(
          self, environment: Mapping[str, str | AbstractSet[str]]
      ) -> bool:
>>>>>>> REPLACE