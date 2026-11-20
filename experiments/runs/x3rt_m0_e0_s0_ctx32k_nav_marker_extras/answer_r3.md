### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _collect_extras(markers: MarkerList, extras: set[str]) -> None:
    """Recursively collect all extra names referenced in a marker tree."""
    for item in markers:
        if isinstance(item, list):
            _collect_extras(item, extras)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            # Determine the variable key (left or right side)
            if isinstance(lhs, Variable):
                key = lhs.value
                # For extras membership ("x" in extras), the literal is on the left
                if key == "extra":
                    if isinstance(rhs, Value):
                        extras.add(canonicalize_name(rhs.value))
                elif key in MARKERS_ALLOWING_SET:
                    # "x" in extras / "x" in dependency_groups
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable):
                key = rhs.value
                if key == "extra":
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
                elif key in MARKERS_ALLOWING_SET:
                    # "extras" on the right side, the literal is on the left
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
=======
def _collect_extras(markers: MarkerList, extras: set[str]) -> None:
    """Recursively collect all extra names referenced in a marker tree."""
    for item in markers:
        if isinstance(item, list):
            _collect_extras(item, extras)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable):
                key = lhs.value
                if key == "extra":
                    if isinstance(rhs, Value):
                        extras.add(canonicalize_name(rhs.value))
                elif key == "extras":
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable):
                key = rhs.value
                if key == "extra":
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
                elif key == "extras":
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE