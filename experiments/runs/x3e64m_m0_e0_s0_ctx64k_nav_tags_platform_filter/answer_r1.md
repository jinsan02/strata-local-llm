수정 내용 요약:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms` 추가
   - `from collections.abc import Iterable` import 추가
   - 시그니처에 `platforms: Iterable[str] | None = None` 파라미터 추가
   - `platforms`가 `None`이 아니면:
     - `str`을 직접 주면 `TypeError` 발생
     - 각 플랫폼 이름을 `.`·`-`·공백 → `_` 치환 + 소문자로 정규화
     - wheel 태그 중 하나라도 정규화된 이름과 일치하거나 `"any"` 플랫폼 태그가 있으면 통과
     - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 발생
   - 기존 동작(기본값 `None`)은 변경 없음