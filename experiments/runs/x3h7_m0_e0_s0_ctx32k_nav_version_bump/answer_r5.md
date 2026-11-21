수정 완료.

### 변경 사항 요약

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- **`bump("major")`**: release의 첫 번째 숫자를 1 올리고 뒤를 모두 0으로 만듦 (예: `1.2.3` → `2.0.0`)
- **`bump("minor")`**: release의 두 번째 숫자를 1 올리고 뒤를 모두 0으로 만듦 (예: `1.2.3` → `1.3.0`, `1.2.3.4` → `1.3.0.0`)
- **`bump("micro")`**: release의 세 번째 숫자를 1 올리고 뒤를 모두 0으로 만듦 (예: `1.2.3` → `1.2.4`, `1` → `1.0.1`)
- release 길이가 부족하면 0을 채워 해당 자리까지 늘림
- epoch는 유지하고, pre/post/dev/local은 모두 버림
- 원래 객체는 불변이며 새 `Version` 인스턴스를 반환
- 유효하지 않은 `part` 값(대소문자 불일치 포함)은 `ValueError` 발생
- 기존 동작은 변경 없음