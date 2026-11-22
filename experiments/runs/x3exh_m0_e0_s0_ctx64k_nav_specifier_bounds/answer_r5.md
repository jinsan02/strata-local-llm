Implementation complete. Here's what I changed in `src/packaging/specifiers.py`:

1. Added type alias `_SpecifierBound` (line ~80)
2. Added helper function `_max_lower()` to merge lower bounds (line ~83)
3. Added helper function `_min_upper()` to merge upper bounds (line ~103)
4. Added helper function `_specifier_bounds()` to compute bounds for a single specifier (line ~123)
5. Added `bounds()` method to `SpecifierSet` class (line ~1336)

The method:
- Raises `ValueError` if any `===` specifier is present
- Iterates over all specifiers, computing individual bounds and merging them (max for lower, min for upper)
- Returns `(None, None)` for empty `SpecifierSet`
- Handles all operators per the spec table, including wildcards (`==V.*`) and compatible (`~=V`) with correct epoch preservation and release-only upper versions