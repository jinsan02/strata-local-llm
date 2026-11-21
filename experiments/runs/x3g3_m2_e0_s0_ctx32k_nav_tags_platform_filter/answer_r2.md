수정 내용을 요약하면:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
2. `from collections.abc import Iterable` import 추가
3. `platforms`가 `None`이 아니면:
   - `str`을 직접 주면 `TypeError` 던짐
   - 제공된 플랫폼 이름들을 `.`·`-`·공백 → `_` 치환 + 소문자로 정규화
   - wheel 태그의 플랫폼도 동일하게 정규화하여 비교
   - 태그 중 하나라도 플랫폼이 `any`이거나 정규화한 제공 플랫폼 중 하나와 일치하면 통과
   - 일치하는 태그가 없으면 `InvalidWheelFilename` 던짐
4. 기존 동작 (`platforms=None`) 은 변경 없음