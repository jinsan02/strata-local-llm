기존 테스트 전체 51524개가 통과했습니다. `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**변경 내용:**
- `src/packaging/version.py` 의 `Version.micor` 속성 아래에 `bump` 메서드 추가
- `"major"` · `"minor"` · `"micro"` 중 하나를 받아 해당 인덱스의 release 숫자를 1 증가시키고 뒤의 숫자는 0으로 리셋
- 존재하지 않는 인덱스일 경우 0을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch 유지, pre/post/dev/local 모두 버림
- 잘못된 `part` 값은 `ValueError` 발생
- 원래 객체는 불변이고 새 `Version` 인스턴스를 반환