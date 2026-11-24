The implementation looks correct. Let me verify the `_collect_extras` method handles the `MarkerLogical` type (which is `"and"` or `"or"` strings) correctly. Looking at the code, the `_collect_extras` method iterates over the `MarkerList` which contains `MarkerAtom | MarkerLogical` items. The `isinstance(item, list)` check handles nested lists, and `isinstance(item, tuple)` handles comparisons. The `"and"` and `"or"` strings would fall through both checks and be ignored, which is correct since they're just logical operators, not comparisons.

Let me also verify that the `MarkerLogical` type is `Literal["and", "or"]` and that our code handles it properly:

Looking at line 94 of `_parser.py`: `MarkerLogical = Literal["and", "or"]`

Our `_collect_extras` method correctly ignores these string literals since they don't match `isinstance(item, list)` or `isinstance(item, tuple)`.

The implementation is complete. Here's a summary of changes:

1. **`src/packaging/markers.py`**:
   - Added `NormalizedName` to the import from `.utils`
   - Added `referenced_extras()` method to the `Marker` class that recursively scans the marker tree and collects all extra names referenced in comparisons with `extra` variable or membership tests against `extras`
   - Added two helper methods: `_collect_extras()` for recursive traversal and `_extract_extra_from_comparison()` for extracting extra names from individual comparisons

2. **`src/packaging/requirements.py`**:
   - Added `NormalizedName` to the import from `.utils`
   - Added `marker_extras` property to the `Requirement` class that returns the result of `self.marker.referenced_extras()` if a marker exists, or an empty `frozenset` otherwise