`packaging.version.Version` 에 메서드 `bump(part: str) -> Version` 을 추가하라.

- `part` 는 `"major"` · `"minor"` · `"micro"` 중 하나다. 각각 release 의 첫째 · 둘째 · 셋째 숫자를 1 올리고, 그 뒤의 release 숫자는 모두 0 으로 만든다.
- release 길이는 유지한다. 올릴 자리가 없으면 0 을 채워 그 자리까지 늘린다. 예: `1` → micro → `1.0.1`, `1.2.3.4` → minor → `1.3.0.0`.
- epoch 는 그대로 둔다. pre · post · dev · local 은 모두 버린다. 예: `2!1.2.3rc1.post2.dev3+abc` → micro → `2!1.2.4`.
- 그 밖의 `part` 값(대소문자가 다른 것 포함)은 `ValueError` 를 던진다.
- 원래 객체는 바뀌지 않고, 결과는 새 `Version` 이다.
- 기존 동작은 바뀌면 안 된다.
