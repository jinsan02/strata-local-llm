The implementation is complete. Here's a summary of the changes made to `src/packaging/utils.py`:

1. **Added import**: `from collections.abc import Iterable` for the type annotation.
2. **Added import**: `_normalize_string` from `.tags` to reuse the same normalization logic.
3. **Added `platforms` parameter** to `parse_wheel_filename` signature: `platforms: Iterable[str] | None = None`.
4. **Updated docstring** with documentation for the new parameter, including behavior details and the `TypeError` case.
5. **Added platform validation logic** after tag parsing:
   - If `platforms` is `str`, raises `TypeError`.
   - Normalizes each platform name using `_normalize_string(p).lower()` (same rule as `packaging.tags`).
   - Checks if any tag's platform is `"any"` or matches a normalized platform name.
   - If no match, raises `InvalidWheelFilename`.
   - If `platforms` is `None`, skips validation (existing behavior preserved).