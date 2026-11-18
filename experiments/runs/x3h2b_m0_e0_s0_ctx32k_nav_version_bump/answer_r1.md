src/packaging/version.py의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `_trim_release` 메서드 직후 (라인 1140 부근) 에 삽입
- `"major"`/`"minor"`/`"micro"` 외의 값은 `ValueError` 발생
- release 튜플을 리스트로 변환해 인덱스를 늘리고 뒤를 0으로 채운 후, `__replace__`로 새 `Version` 객체 반환 (epoch 유지, pre/post/dev/local 버림)