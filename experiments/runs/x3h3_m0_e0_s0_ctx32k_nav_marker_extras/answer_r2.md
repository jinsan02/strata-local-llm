EDIT: src/packaging/markers.py
<<<<<<< SEARCH
          return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
          return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return the extra names referenced in this marker.

        This extracts all extra names from ``extra == "name"``, ``"name" == extra``,
        and ``"name" in extras`` expressions within the marker, returning them as a
        :class:`frozenset` of canonicalized names.

        .. versionadded:: 26.5
        """
        extras: set[str] = self._extract_referenced_extras(self._markers)
        return frozenset(extras)

    @classmethod
    def _extract_referenced_extras(cls, markers: MarkerList) -> set[str]:
        """Recursively extract extra names from a marker tree."""
        extras: set[str] = set()
        for item in markers:
            if isinstance(item, tuple):
                lhs, op, rhs = item
                # Handle ``extra == "val"`` or ``"val" == extra``
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.add(canonicalize_name(rhs.value))
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
                
                # Handle ``"val" in extras``
                if isinstance(rhs, Variable) and rhs.value == "extras":
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
            elif isinstance(item, list):
                extras.update(cls._extract_referenced_extras(item))
        return extras


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )
=======
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the extra names referenced in this requirement's marker.
        
        Returns an empty frozenset if the requirement has no marker.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE