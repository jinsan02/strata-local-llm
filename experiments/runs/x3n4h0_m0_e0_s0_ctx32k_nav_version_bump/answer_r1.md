수정 완료했습니다. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**변경 내용:**
- `micro` 속성 뒤에 `bump()` 메서드 추가 (총 53줄 추가)
- `part`가 `"major"`/`"minor"`/`"micro"` 외의 값이면 `ValueError` 발생
- 해당 위치의 release 숫자를 +1 하고, 그 이후의 모든 숫자를 0으로 설정
- 올릴 자리가 없으면 해당 길이까지 0으로 확장 (예: `1` → micro → `1.0.1`)
- pre/post/dev/local 은 모두 버리고 epoch 는 유지
- `__replace__`를 사용하여 새 `Version` 객체 반환 (원본 불변)