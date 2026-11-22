The implementation is complete. Here's a summary of the changes made:

1. **Added `InvalidGroupName` exception class** (subclass of `ValueError`) between `DuplicateGroupNames` and `CyclicDependencyGroup`.

2. **Added `InvalidGroupName` to `__all__`** for public export.

3. **Imported `_validate_regex`** from `packaging.utils` (the same regex used for core metadata `Name` field validation) and added `utils` to `__lazy_modules__`.

4. **Added `_validate_group_name()` helper function** that uses `_validate_regex.fullmatch()` to validate group names, raising `InvalidGroupName` with the name in `repr` form if invalid.

5. **Updated `_normalize_group_names()`** to validate each group name before normalization. Invalid names are caught and added to the error collector (alongside other errors like duplicates), so they're reported together in an `ExceptionGroup` during `DependencyGroupResolver.__init__`.

6. **Updated `DependencyGroupResolver.lookup()` and `resolve()`** to call `_validate_group_name()` immediately before normalizing. This ensures a single `InvalidGroupName` is raised directly (not collected) when an invalid name is passed to these methods.