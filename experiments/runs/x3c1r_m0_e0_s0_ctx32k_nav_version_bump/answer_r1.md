### 수정 내용 요약

**파일**: `src/packaging/version.py`

`Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `"major"` → release[0] 을 1 증가, 이후 모두 0 (예: `1.2.3` → `2.0.0`)
- `"minor"` → release[1] 을 1 증가, 이후 모두 0 (예: `1.2.3` → `1.3.0`, `1.2.3.4` → `1.3.0.0`)
- `"micro"` → release[2] 을 1 증가, 이후 모두 0 (예: `1` → `1.0.1`, `1.2.3` → `1.2.4`)
- epoch 는 그대로 유지, pre/post/dev/local 은 모두 제거
- 올바르지 않은 `part` 값이면 `ValueError` 발생
- 기존 객체는 불변, 새 `Version` 반환