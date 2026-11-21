수정을 완료했습니다. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`** 의 `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
2. `platforms`가 `None`이 아니면:
   - `str`을 직접 주면 `TypeError` 던짐
   - `_normalize_string(p).lower()`로 각 플랫폼 이름을 정규화 (`.`, `-`, ` ` → `_` + 소문자)
   - 태그의 플랫폼 중 하나가 정규화된 이름과 일치하거나 `any`이면 통과
   - 일치하는 것이 없으면 `InvalidWheelFilename` 던짐
3. 기존 동작(`platforms=None`)은 변경 없음
4. `Iterable` 타입과 `_normalize_string` 함수를 import 함