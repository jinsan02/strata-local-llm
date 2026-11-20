### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __hash__(self) -> int:
        return hash((self.name, frozenset(self.extras), self.specifier, self.url, self.marker))

    def __str__(self) -> str:
=======
    def __hash__(self) -> int:
        return hash((self.name, frozenset(self.extras), self.specifier, self.url, self.marker))

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in the marker.

        Returns an empty :class:`frozenset` if there is no marker, otherwise
        returns the result of :meth:`Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def __str__(self) -> str:
>>>>>>> REPLACE