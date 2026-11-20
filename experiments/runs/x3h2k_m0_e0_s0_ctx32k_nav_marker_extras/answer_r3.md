### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
      return any(all(item) for item in groups)


def _format_full_version(info: sys._version_info) -> str:
=======
      return any(all(item) for item in groups)


def _collect_extras(markers: MarkerList) -> frozenset[str]:
    """Collect all extra names referenced in a marker tree."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras.update(_collect_extras(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value in ("extra", "extras"):
                if isinstance(rhs, Value):
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value in ("extra", "extras"):
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
    return frozenset(extras)


def _format_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this marker.

        Collects every extra name appearing in ``extra == "x"``,
        ``"x" == extra``, ``extra != "x"``, ``"x" in extras``, and
        ``"x" not in extras`` comparisons, normalized to canonical form.
        """
        return _collect_extras(self._markers)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              and self.marker == other.marker
          )
=======
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Extra names referenced in this requirement's marker.

        Returns an empty frozenset if there is no marker.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE