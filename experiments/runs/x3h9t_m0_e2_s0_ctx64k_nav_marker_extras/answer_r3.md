EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in the marker.

        Returns a :class:`frozenset` of normalized extra names found in
        the marker. If the requirement has no marker, returns an empty
        :class:`frozenset`.

        .. versionadded:: 26.4
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
=======
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in the marker.

        Returns a :class:`frozenset` of normalized extra names found in
        the marker. If the requirement has no marker, returns an empty
        :class:`frozenset`.

        .. versionadded:: 26.4
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE