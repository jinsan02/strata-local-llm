수정 완료. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 일 때 각각 release 튜플의 0, 1, 2 번째 인덱스를 1 증가시키고 뒤의 모든 인덱스를 0 으로 설정한다.
- 인덱스가 release 길이보다 크면 0 을 채워 확장한다.
- `__replace__` 를 사용해 epoch 는 유지하고 pre/post/dev/local 은 모두 None 으로 버린다.
- 그 외의 `part` 값은 `ValueError` 를 던진다.
- 원래 객체는 불변이고 새 `Version` 인스턴스를 반환한다.