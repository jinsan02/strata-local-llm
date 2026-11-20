### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _pep440_python_full_version(python_full_version: str) -> str:
=======
def _collect_extras(markers: MarkerList) -> frozenset[str]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.update(_collect_extras(item))
        elif isinstance(item, tuple):
            lhs, _op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                if isinstance(lhs, Value):
                    extras.add(canonicalize_name(lhs.value))
            elif isinstance(lhs, Variable) and lhs.value == "extras":
                if isinstance(rhs, Value):
                    extras.add(canonicalize_name(rhs.value))
    return frozenset(extras)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    def _iter_parts(self, name: str) -> Iterator[str]:
=======
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    @property
    def marker_extras(self) -> frozenset[str]:
        """The extra names referenced in this requirement's marker.
        
        Returns an empty frozenset if the marker is ``None``.
        
        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE