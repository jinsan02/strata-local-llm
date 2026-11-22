The implementation is complete. Here's a summary of the changes made to `src/packaging/dependency_groups.py`:

1. **Added import**: `from .utils import _validate_regex` — reuses the existing core metadata `Name` validation regex.

2. **Added `InvalidGroupName` exception** (line 47–54): A new `ValueError` subclass for invalid group names.

3. **Added to `__all__`**: `"InvalidGroupName"` (line 25).

4. **`_normalize_group_names()`**: Now validates each group name with `_validate_regex.fullmatch()`. Invalid names trigger `InvalidGroupName` errors collected via `_ErrorCollector`, reported as a batch in `__init__`.

5. **`lookup()`**: Validates the group name with `_validate_regex.fullmatch()` before any processing, raising `InvalidGroupName` immediately if invalid.

6. **`resolve()`**: Same validation — raises `InvalidGroupName` immediately for invalid names.