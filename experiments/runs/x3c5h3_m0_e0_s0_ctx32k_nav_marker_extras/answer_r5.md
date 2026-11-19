### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def __or__(self, other: Marker) -> Marker:
        """Combine this marker with another using ``or``.

        .. versionadded:: 26.1
        """
        if not isinstance(other, Marker):
            return NotImplemented
        return self._from_markers(_join_markers(self._markers, "or", other._markers))

    def evaluate(
=======
    def __or__(self, other: Marker) -> Marker:
        """Combine this marker with another using ``or``.

        .. versionadded:: 26.1
        """
        if not isinstance(other, Marker):
            return NotImplemented
        return self._from_markers(_join_markers(self._markers, "or", other._markers))

    def referenced_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this marker as a normalized ``frozenset``.

        Looks for comparisons between ``extra`` and values, as well as membership checks like
        ``"foo" in extras`` or ``"bar" not in extras`` across the entire expression (including
        nested ``and``/``or`` blocks). Extra names are canonicalized (lowercased, hyphens to underscores).

        Returns:
            A frozenset of normalized extra names. Returns an empty frozenset if no extras
            are referenced by this marker.

        .. versionadded:: 26.5
        """
        return _marker_referenced_extras(self._markers)

    def evaluate(
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the extra names referenced in this requirement's marker.

        If the requirement has no marker, returns an empty ``frozenset``.
        Otherwise, delegates to :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the extra names referenced in this requirement's marker.

        If the requirement has no marker, returns an empty ``frozenset``.
        Otherwise, delegates to :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()