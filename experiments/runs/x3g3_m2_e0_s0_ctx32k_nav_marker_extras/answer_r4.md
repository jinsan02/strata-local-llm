### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    return any(all(item) for item in groups)


def _format_full_version(info: sys._version_info) -> str:
=======
    return any(all(item) for item in groups)


def _referenced_extras(markers: MarkerList) -> frozenset[str]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras.update(_referenced_extras(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
    return frozenset(extras)


def _format_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
          .. versionadded:: 26.4
          """
          return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
          .. versionadded:: 26.4
          """
          return _evaluate_markers(self._markers, environment)

      def referenced_extras(self) -> frozenset[str]:
          """Return all extra names referenced in this marker.

          Scans the entire marker expression (including nested ``and``/``or``
          and parenthesised sub-expressions) for every comparison involving the
          ``extra`` variable — both equality/inequality forms (``extra == "x"``,
          ``"x" == extra``, ``extra != "x"``, ``"x" != extra``) and membership
          forms (``"x" in extras``, ``"x" not in extras``).  Returns the names
          as a :class:`frozenset` of :term:`normalized <Normalized Name>` strings.

          A marker that does not reference any extra returns an empty frozenset.

          .. versionadded:: 26.5
          """
          return _referenced_extras(self._markers)


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

          Returns an empty :class:`frozenset` if there is no marker.
          """
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()
>>>>>>> REPLACE