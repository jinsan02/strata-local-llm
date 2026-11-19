수정 내용 요약:

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다 (약 50줄). 

- `part`가 `"major"`/`"minor"`/`"micro"`일 때 각각 release의 첫·둘째·셋째 숫자를 1 올리고, 뒤의 모든 숫자를 0으로 만든다.
- 올릴 자리가 release 길이보다 크면 0을 채워 확장한다 (예: `1` → micro → `1.0.1`).
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 None으로 클리어한다.
- 유효하지 않은 `part` 값이면 `ValueError`를 던진다.
- 기존 객체는 불변이며 새 `Version` 인스턴스를 반환한다.
- 내부적으로 동일한 방식으로 새 객체를 만드는 패턴(`__class__.__new__`)을 사용하며, `__replace__`를 재사용해 코드를 간결하게 했다.