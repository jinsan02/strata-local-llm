The implementation looks correct. Let me summarize what was changed:

1. **`src/packaging/markers.py`**:
   - Added `NormalizedName` to the import from `.utils`
   - Added `Marker.referenced_extras()` method that recursively traverses the marker tree and collects all extra names referenced in comparisons involving `extra` or `extras` variables, returning them as a `frozenset[NormalizedName]`
   - Added a static helper method `Marker._collect_extras()` for the recursive traversal

2. **`src/packaging/requirements.py`**:
   - Added `NormalizedName` to the import from `.utils`
   - Added `Requirement.marker_extras` property that returns an empty `frozenset` if there's no marker, otherwise returns `self.marker.referenced_extras()`