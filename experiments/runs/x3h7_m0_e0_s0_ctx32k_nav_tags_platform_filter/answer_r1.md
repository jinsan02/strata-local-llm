수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`**:
   - `from typing import Iterable, NewType, cast` — `Iterable` 추가
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `None`이 아니면:
     - `str`을 직접 주면 `TypeError` 던짐
     - 각 플랫폼 이름을 `.`, `-`, ` ` → `_`로 바꾸고 소문자 정규화하여 `frozenset`으로 저장
     - 태그들 중 `platform == "any"`이거나 정규화한 플랫폼 이름이 `normalized_platforms`에 있으면 통과
     - 하나도 없으면 `InvalidWheelFilename` 던짐
   - `platforms=None` (기본값)이면 기존 동작과 동일하게 통과
   - docstring에 `platforms` 파라미터 설명과 `.. versionchanged:: 26.5` 주석 추가