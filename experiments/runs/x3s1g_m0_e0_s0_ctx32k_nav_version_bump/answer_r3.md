### 수정 내용 요약

**파일**: `src/packaging/version.py`

**변경 사항**:
- `Version` 클래스에 `bump(part: str) -> Version` 메서드 추가 (라인 596~657 부근, `__replace__` 메서드 뒤)

**메서드 동작**:
- `part="major"`: release의 첫 번째 숫자를 1 증가, 이후 모두 0 (`1.2.3` → `2.0.0`)
- `part="minor"`: release의 두 번째 숫자를 1 증가, 이후 모두 0 (`1.2.3` → `1.3.0`)
- `part="micro"`: release의 세 번째 숫자를 1 증가, 이후 모두 0 (`1.2.3` → `1.2.4`)
- release 길이가 부족하면 0을 채워 자릿수 확장 (`1` → micro → `1.0.1`, `1.2.3.4` → minor → `1.3.0.0`)
- epoch는 유지, pre/post/dev/local은 모두 버림
- 잘못된 `part` 값(`ValueError`)
- 불변성 보장 (`__replace__` 사용)