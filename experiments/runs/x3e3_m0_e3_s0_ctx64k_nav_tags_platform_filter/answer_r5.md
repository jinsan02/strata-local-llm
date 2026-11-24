수정 내용:

**`src/packaging/utils.py`**
- `typing.Iterable` import 추가
- `_normalize_string`을 `packaging.tags`에서 import
- `parse_wheel_filename`에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
- `platforms`가 `str`인 경우 `TypeError` 던짐
- `platforms`가 `None`이 아니면 태그의 플랫폼 이름을 `_normalize_string` + `.lower()`로 정규화해 비교. `any` 플랫폼 태그는 항상 통과. 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 던짐
- 기존 동작(`platforms=None`)은 변경 없음