### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def _iter_parts(self, name: str) -> Iterator[str]:
        yield name
=======
    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in the requirement's marker.

        Returns an empty :class:`frozenset` if the requirement has no marker,
        otherwise returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def _iter_parts(self, name: str) -> Iterator[str]:
        yield name
>>>>>>> REPLACE