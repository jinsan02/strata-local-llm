The implementation is complete. Here's a summary of the changes:

1. **`src/packaging/markers.py`** — Added `Marker.referenced_extras()` method and its helper `Marker._collect_extras()` static method:
   - `referenced_extras()` traverses the marker tree and collects all extra names referenced in comparisons (`extra == "x"`, `"x" == extra`, `extra != "x"`, etc.) and membership tests (`"x" in extras`, `"x" not in extras`).
   - Names are normalized via `canonicalize_name()` and returned as a `frozenset[str]`.
   - The helper `_collect_extras()` recursively walks the tree, handling tuples (atoms), strings (and/or operators), and lists (nested/parenthesized groups).

2. **`src/packaging/requirements.py`** — Added `Requirement.marker_extras` property:
   - Returns `frozenset()` if the requirement has no marker.
   - Otherwise delegates to `self.marker.referenced_extras()`.

No existing behavior (stringification, comparison, hashing, evaluation) was modified.