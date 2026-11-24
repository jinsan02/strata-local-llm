수정 완료. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

**변경 내용 요약:**
- `Version` 클래스에 `bump` 메서드 추가 (약 45 줄)
- `part` 가 `"major"`/`"minor"`/`"micro"` 일 때 각각 release 의 첫/둘/셋째 숫자를 1 증가시키고 이후 숫자를 0 으로 설정
- release 길이가 부족하면 0 을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch 는 유지하고, pre/post/dev/local 은 모두 None 으로 버림
- 유효하지 않은 `part` 값은 `ValueError` 던짐
- `__replace__` 를 사용해 원래 객체는 변경하지 않고 새 `Version` 반환