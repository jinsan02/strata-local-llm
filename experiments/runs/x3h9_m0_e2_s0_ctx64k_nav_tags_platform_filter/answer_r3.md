The implementation is complete. Here's a summary of the changes made to `src/packaging/utils.py`:

1. **Added import**: `from collections.abc import Iterable`

2. **Added helper function** `_normalize_platform(string: str) -> str`: Normalizes platform names by replacing `.`, `-`, and spaces with `_`, then lowercasing — matching the same normalization used in `packaging.tags._normalize_string`.

3. **Modified `parse_wheel_filename`**:
   - Added keyword-only parameter `platforms: Iterable[str] | None = None`
   - Added docstring for the `platforms` parameter and `TypeError` raise
   - Added validation logic: if `platforms` is not `None`, checks that it's not a single `str` (raises `TypeError`), normalizes each platform name, and verifies at least one tag's platform matches (or is `"any"`). Raises `InvalidWheelFilename` on mismatch.
   - Existing behavior is unchanged when `platforms` is `None` (default).