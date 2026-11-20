### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None

    def __replace__(
=======
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the set of extra names referenced by the requirement's marker.

        Returns an empty :class:`frozenset` if the requirement has no marker,
        otherwise returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def __replace__(
>>>>>>> REPLACE