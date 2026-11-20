### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
      env["python_full_version"] = _pep440_python_full_version(python_full_version)
      return env
=======
      env["python_full_version"] = _pep440_python_full_version(python_full_version)
      return env


def _get_referenced_extras(markers: MarkerList) -> frozenset[NormalizedName]:
    extras: set[NormalizedName] = set()
    for marker in markers:
        if isinstance(marker, list):
            extras |= _get_referenced_extras(marker)
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
    return frozenset(extras)
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Marker):
            return NotImplemented

        return str(self) == str(other)
=======
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Marker):
            return NotImplemented

        return str(self) == str(other)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return a frozenset of all extra names referenced in the marker."""
        return _get_referenced_extras(self._markers)
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

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
        """Return a frozenset of all extra names referenced in the marker, or an empty frozenset if there is no marker."""
        return self.marker.referenced_extras() if self.marker else frozenset()
>>>>>>> REPLACE