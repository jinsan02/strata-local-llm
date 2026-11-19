`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다. 이 메서드는 다음과 같이 동작한다:

- `major`: release[0] 을 1 증가시키고 뒤 모두 0 으로 설정 (예: `1.2.3` → `2.0.0`)
- `minor`: release[1] 을 1 증가시키고 뒤 모두 0 으로 설정 (예: `1.2.3` → `1.3.0`)
- `micro`: release[2] 을 1 증가시키고 뒤 모두 0 으로 설정 (예: `1.2.3` → `1.2.4`)
- 요청한 위치가 현재 release 에 없으면 0 을 채워 그 자리까지 늘린 후 1 로 설정 (예: `1` → micro → `1.0.1`)
- epoch 는 유지되고, pre/post/dev/local 은 모두 버린다 (예: `2!1.2.3rc1.post2.dev3+abc` → micro → `2!1.2.4`)
- 유효하지 않은 `part` 값은 `ValueError` 를 던진다
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다