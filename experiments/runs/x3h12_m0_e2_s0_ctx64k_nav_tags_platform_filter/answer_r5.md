수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`**:
   - `from collections.abc import Iterable` import 추가
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `str`이면 `TypeError` 발생
   - 플랫폼 이름은 `.`, `-`, 공백을 `_`로 바꾸고 소문자로 정규화하여 비교
   - 태그 중 `any` 플랫폼이 있거나 정규화된 플랫폼 중 하나와 일치하면 통과
   - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 발생
   - 기존 동작(파라미터 생략 시)은 변경 없음