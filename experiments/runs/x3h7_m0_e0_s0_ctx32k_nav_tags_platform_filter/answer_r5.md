The changes are complete. Here's a summary of what was modified in `src/packaging/utils.py`:

1. **Added import**: `from collections.abc import Iterable` and `_normalize_string` from `packaging.tags`.

2. **Added `platforms` parameter** to `parse_wheel_filename` signature: `platforms: Iterable[str] | None = None`.

3. **Added validation logic** after existing filename/tag parsing:
   - If `platforms` is a single `str`, raises `TypeError`.
   - Normalizes both the provided platform names and wheel platform tags using `_normalize_string().lower()` (same rule as `packaging.tags`).
   - If any platform tag is `"any"`, the check passes (even for empty `platforms` iterable).
   - Otherwise, checks if the intersection of normalized wheel platform tags and normalized provided platforms is non-empty. If not, raises `InvalidWheelFilename`.

4. **Updated docstring** with description of the `platforms` parameter, its `TypeError` case, and a `.. versionadded:: 26.4` note.