`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나이면 해당 인덱스의 release 값을 1 올리고, 뒤의 모든 값을 0 으로 만듭니다.
- 올릴 자리가 release 튜플보다 긴 경우 0 을 채워 길이를 확장합니다.
- epoch 는 그대로 유지되고, pre/post/dev/local 은 모두 None(버림) 으로 설정됩니다.
- 그 외의 `part` 값은 `ValueError` 를 던집니다.
- 원래 객체는 수정되지 않고 새 `Version` 인스턴스를 반환합니다.