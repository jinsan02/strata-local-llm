수정 사항을 요약하면:

1. **`src/packaging/utils.py`**:
   - `from collections.abc import Iterable` import 추가
   - `_normalize_platform(platform)` 헬퍼 함수 추가: `.`, `-`, ` `를 `_`로 바꾸고 소문자로 정규화
   - `parse_wheel_filename()`에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `str`이면 `TypeError` 던짐
   - `platforms`가 `None`이 아니면, 제공된 플랫폼 이름들을 정규화한 집합과 wheel 태그들의 플랫폼을 비교. 태그 중 하나라도 플랫폼이 `"any"`이거나 정규화된 이름이 제공된 플랫폼 집합에 있으면 통과, 아니면 `InvalidWheelFilename` 던짐
   - 기존 동작(기본값 `None`)은 변경 없음 — 기존 테스트 317개 모두 통과