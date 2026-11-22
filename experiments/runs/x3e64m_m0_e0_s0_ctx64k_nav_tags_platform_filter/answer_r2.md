수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`**:
   - `typing.Iterable` import 추가
   - `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
   - `platforms`가 `None`이 아니면:
     - `str`을 주면 `TypeError` 던짐
     - 각 플랫폼 이름을 `.`, `-`, 공백을 `_`로 바꾸고 소문자로 정규화하여 `frozenset`으로 저장
     - 태그 중 `platform == "any"`이거나 정규화된 플랫폼 집합에 속하는 것이 있으면 통과, 아니면 `InvalidWheelFilename` 던짐
   - 기존 동작(`platforms=None`)은 변경 없음
   - docstring에 파라미터 설명과 `.. versionadded:: 26.4` 주석 추가