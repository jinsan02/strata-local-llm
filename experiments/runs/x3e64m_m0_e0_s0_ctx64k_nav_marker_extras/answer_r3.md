### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        if self.marker:
            yield f"; {self.marker}"

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
        if self.marker:
            yield f"; {self.marker}"

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this requirement's marker.

        Returns an empty :class:`frozenset` if there is no marker.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE

`src/packaging/requirements.py`에 `Requirement.marker_extras` 속성을 추가했습니다. `markers.py`의 `referenced_extras()` 메서드 추가는 이전 단계에서 완료했으며, 기존 문자열화·비교·해시·평가 동작은 모두 유지됩니다.