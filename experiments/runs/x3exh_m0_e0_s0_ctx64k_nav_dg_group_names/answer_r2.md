The implementation is complete. Here's a summary of the changes made to `src/packaging/dependency_groups.py`:

1. **Added `InvalidGroupName` exception** (line 86-92): A new `ValueError` subclass for invalid group names, with docstring and version tag.

2. **Added to `__all__`** (line 26): `InvalidGroupName` is now exported.

3. **Imported `_validate_regex`** (line 18): Imported from `.utils` to reuse the core metadata `Name` validation regex (no new regex created).

4. **Added `utils` to `__lazy_modules__`** (line 10): For lazy loading support.

5. **Added `_validate_group_name()` helper** (lines 332-338): Validates a group name using `_validate_regex.fullmatch()`, raising `InvalidGroupName` with the name in `repr` form if invalid.

6. **Modified `_normalize_group_names()`** (lines 348-352): Each group name is validated before normalization. Invalid names are caught and collected via the existing `_ErrorCollector`, so they're reported together with other errors (like `DuplicateGroupNames`) in an `ExceptionGroup`.

7. **Added validation to `lookup()`** (line 159): `_validate_group_name(group)` is called before any other processing, raising `InvalidGroupName` immediately as a single exception.

8. **Added validation to `resolve()`** (line 173): Same as `lookup()` — raises `InvalidGroupName` immediately for invalid names.