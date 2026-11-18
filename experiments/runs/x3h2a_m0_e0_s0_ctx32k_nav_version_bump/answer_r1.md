수정을 완료했습니다. `packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**주요 변경 사항:**
- `src/packaging/version.py`: `Version` 클래스 내에 `bump()` 메서드 추가 (1112~1167 행)
  - `"major"`, `"minor"`, `"micro"` 외의 값은 `ValueError` 발생
  - epoch 는 유지, pre/post/dev/local 은 모두 버림
  - release 길이 부족 시 0 으로 채워 확장