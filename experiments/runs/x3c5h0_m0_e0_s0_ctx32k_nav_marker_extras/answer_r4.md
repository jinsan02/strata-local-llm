### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def _iter_parts(self, name: str) -> Iterator[str]:
=======
    @property
    def marker_extras(self) -> frozenset[str]:
        """Extra names referenced in this requirement's marker.

        Returns an empty :class:`frozenset` if there is no marker.
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE