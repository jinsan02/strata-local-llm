### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              and self.url == other.url
              and self.marker == other.marker
          )
=======
              and self.url == other.url
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return the extra names referenced by this requirement's marker.

        If the requirement has no marker, returns an empty ``frozenset``.
        Otherwise, returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE