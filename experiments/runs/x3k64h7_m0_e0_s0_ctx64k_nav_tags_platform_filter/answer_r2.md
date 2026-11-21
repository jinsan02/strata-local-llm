The implementation is complete. Here's a summary of the changes made to `src/packaging/utils.py`:

1. **Added import**: `from collections.abc import Iterable` (line 10)

2. **Added helper function** `_normalize_platform(platform: str) -> str` (lines 203-208): Normalizes platform names by replacing `.`, `-`, and spaces with `_`, then lowercasing — matching the same rules used by `packaging.tags`.

3. **Modified `parse_wheel_filename`** (lines 211-344):
   - Added keyword-only parameter `platforms: Iterable[str] | None = None`
   - Updated docstring with parameter description and `.. versionadded:: 26.4`
   - After existing validation passes, if `platforms is not None`:
     - Raises `TypeError` if `platforms` is a bare `str`
     - Normalizes each platform name and builds a set
     - Checks if any tag has platform `"any"` or if any normalized tag platform matches the normalized set
     - Raises `InvalidWheelFilename` if no match is found
   - Returns the same tuple as before when `platforms` is `None` (unchanged behavior)