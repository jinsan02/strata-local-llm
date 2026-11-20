`src/packaging/version.py`의 `Version` 클래스에 `bump(part)` 메서드를 추가했습니다.

- 메서드는 `micro` property 뒤, `_trim_release()` 앞에 삽입했습니다.
- `part`가 `"major"`/`"minor"`/`"micro"` 외의 값(대소문자 포함)이면 `ValueError`를 던집니다.
- 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자는 0으로 만든 후 그 길이만큼 유지합니다.
- 기존 객체를 건드리지 않고 `__replace__(..., pre=None, post=None, dev=None, local=None)`으로 새 `Version`을 반환하므로 epoch는 그대로 유지되고 pre/post/dev/local은 모두 버려집니다.