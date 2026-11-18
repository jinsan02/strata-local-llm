The `bump` method has been successfully added to the `Version` class. Let me verify the implementation handles all the specified cases correctly by reviewing it once more:

1. **`part` validation**: Only `"major"`, `"minor"`, `"micro"` are accepted; anything else (including case variations like `"Major"`) raises `ValueError`. ✓
2. **Increment logic**: The corresponding release index is incremented by 1, and all subsequent indices are zeroed. ✓
3. **Length maintenance**: When the target index exists in the release tuple, length is preserved. ✓
4. **Extension when needed**: If the requested position doesn't exist (e.g., `Version("1")` with `"micro"`), zeros are padded up to that index. ✓
5. **Epoch preserved**: Passed through unchanged. ✓
6. **Pre/post/dev/local stripped**: All set to `None`. ✓
7. **Immutability**: Uses `__replace__` which returns a new object (or `self` if nothing changed — though for bump, the release always changes). ✓

**수정 내용**: `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다. `_trim_release` 메서드 앞에 위치하며, `__replace__`를 활용해 새 `Version` 객체를 반환합니다.