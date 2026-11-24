The implementation is complete. Here's a summary of the changes made to `src/packaging/utils.py`:

1. **Added import**: `from collections.abc import Iterable` and `_normalize_string` from `.tags`.

2. **Added `platforms` parameter** to `parse_wheel_filename`:
   - Signature: `platforms: Iterable[str] | None = None`
   - If `platforms` is a `str`, raises `TypeError`
   - If `platforms` is not `None`, normalizes each platform name using `_normalize_string(p).lower()` (replaces `.`, `-`, ` ` with `_` and lowercases), stored in a `frozenset`
   - After all existing filename validation passes, checks platform tags:
     - If any tag has platform `"any"`, it always passes (even with empty `platforms` iterable)
     - Otherwise, at least one tag's platform must be in the normalized platforms set
     - If no match, raises `InvalidWheelFilename`
   - Returns the same tuple as before when no platform filtering is needed

3. **Updated docstring** with parameter description, `TypeError` raise documentation, and `.. versionadded:: 26.5` for the `platforms` parameter.