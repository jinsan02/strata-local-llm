### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            self.marker._serialized = None

    def __replace__(
=======
            self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the set of extra names referenced in the marker.

        Returns an empty frozenset if the requirement has no marker.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __replace__(
>>>>>>> REPLACE

`src/packaging/markers.py`에 `Marker.referenced_extras()` 메서드와 내부 순환 로직 `_collect_extras()`를 추가했습니다.
`src/packaging/requirements.py`에 `Requirement.marker_extras` 속성을 추가했습니다.
기존 문자열화, 비교, 해시, 평가 동작은 변경하지 않았습니다.