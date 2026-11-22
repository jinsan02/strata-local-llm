The implementation is complete. Here's a summary of the changes made to `src/packaging/dependency_groups.py`:

1. **Added `InvalidGroupName` exception class** (line 47-52): A new `ValueError` subclass for invalid group names.

2. **Added to `__all__`** (line 25): Exported `InvalidGroupName`.

3. **Imported `_validate_regex`** (line 17): Imported the same regex from `packaging.utils` that validates core metadata `Name` fields.

4. **Added `_validate_group_name()` helper** (line 327-329): Uses `_validate_regex.fullmatch()` to check if a name follows the core metadata `Name` field rules.

5. **Updated `_normalize_group_names()`** (line 347-348): Validates each group name and adds `InvalidGroupName` errors to the `_ErrorCollector`, which collects them alongside other errors (like duplicates) and raises them together via `ExceptionGroup`.

6. **Updated `lookup()`** (line 157-158): Checks group name validity before any processing, raising `InvalidGroupName` as a single exception.

7. **Updated `resolve()`** (line 173-174): Same as `lookup()` — checks group name validity before any processing, raising `InvalidGroupName` as a single exception.