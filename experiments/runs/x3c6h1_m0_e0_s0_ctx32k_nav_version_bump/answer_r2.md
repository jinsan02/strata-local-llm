수정 완료했습니다. 변경 사항을 요약하면 다음과 같습니다:

**파일**: `src/packaging/version.py` (Version 클래스 내)

**추가한 메서드**: `bump(part: str) -> Version`

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스(0, 1, 2)의 release 숫자를 1 증가시키고, 뒤의 모든 숫자를 0 으로 만듭니다.
- 요청된 자리가 현재 release 길이보다 길면 0 으로 채워 늘립니다 (예: `1` → micro → `1.0.1`).
- epoch 는 유지하고, pre/post/dev/local 은 모두 버립니다 (`__replace__` 로 새 Version 반환).
- 유효하지 않은 `part` 값은 `ValueError` 를 던집니다.