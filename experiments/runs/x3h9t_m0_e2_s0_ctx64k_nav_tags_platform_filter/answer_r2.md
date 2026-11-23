다음과 같이 수정했습니다:

1. **`src/packaging/utils.py`**:
   - `typing.NewType` import에 `Iterable` 추가
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `str`이면 `TypeError` 던짐
   - `platforms`가 `None`이 아니면, 주어진 플랫폼 이름들을 정규화(`.` `- ` ` ` → `_`, 소문자)한 집합을 만들고, 태그의 플랫폼이 `any`이거나 정규화한 이름과 일치하는지 확인. 일치하면 통과, 아니면 `InvalidWheelFilename` 던짐
   - 기존 동작(확장자, 이름, 버전, 빌드번호, 태그 검사)은 그대로 유지됨