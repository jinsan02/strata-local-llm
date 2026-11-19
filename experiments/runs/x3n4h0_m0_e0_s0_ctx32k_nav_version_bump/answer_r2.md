수정 사항을 요약하면 다음과 같습니다:

**파일:** `src/packaging/version.py`

**변경 내용:** `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part` 값이 `"major"` → 인덱스 0, `"minor"` → 인덱스 1, `"micro"` → 인덱스 2로 매핑
- 해당 인덱스가 release 튜플에 없으면 0을 채워 연장 (예: `(1,)` → micro → `(1, 0, 1)`)
- 인덱스 부분만 1 증가시키고 그 뒤의 모든 요소는 0으로 초기화
- epoch는 그대로 유지하고 pre/post/dev/local은 모두 무시
- 유효하지 않은 `part` 값(대소문자 포함)에 대해 `ValueError` 발생
- 기존 객체는 불변이며 새 `Version` 인스턴스를 반환