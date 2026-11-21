수정 완료.

변경 사항 요약:
1. `src/packaging/utils.py`의 import에 `Iterable` 추가하고 `tags._normalize_string`을 import
2. `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
3. `platforms`가 `None`이 아니면:
   - `str`을 주면 `TypeError` 던짐
   - 주어진 플랫폼 이름들을 `_normalize_string` + `.lower()`로 정규화
   - 태그의 플랫폼 이름도 동일하게 정규화하여 비교
   - 교집합이 있거나 태그에 `any`가 있으면 통과, 아니면 `InvalidWheelFilename` 던짐