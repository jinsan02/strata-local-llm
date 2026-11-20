### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    def _iter_parts(self, name: str) -> Iterator[str]:
=======
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    @property
    def marker_extras(self) -> frozenset[str]:
        """The extra names referenced in the requirement's marker.

        Returns ``frozenset()`` if there is no marker.
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE

`packaging.markers.Marker`에 `referenced_extras()` 메서드와 `_extract_referenced_extras()` 도우미 함수를 추가했고, `packaging.requirements.Requirement` 클래스에 `marker_extras` 속성(property)을 구현했습니다. 기존 문자열화, 평가, 해시, 비교 동작은 변경하지 않았습니다.