수정을 완료했습니다. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**변경 사항 요약:**
- `Version` 클래스의 `micro` 속성(1110 줄) 직후에 `bump` 메서드 추가
- `part` 가 `"major"`/`"minor"`/`"micro"` 인지 검증하고, 해당 인덱스의 release 숫자를 1 증가시킨 후 뒤의 모든 숫자를 0 으로 설정
- release 길이가 부족하면 0 을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch 는 유지하고, pre/post/dev/local 은 모두 None 으로 초기화
- 유효하지 않은 `part` 값은 `ValueError` 발생
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스 반환