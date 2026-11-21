수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`** 의 `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
2. `typing.Iterable` import 추가
3. 기존 검사(확장자, dash 수, 이름, 버전, 빌드 번호, 태그)가 먼저 실행된 후, `platforms`가 `None`이 아니면:
   - `platforms`가 `str`이면 `TypeError` 던짐
   - 제공된 플랫폼 이름들을 정규화(`.`·`-`·공백 → `_`, 소문자)하여 `frozenset`으로 저장
   - 태그 중 하나라도 `platform == "any"`이거나 정규화된 플랫폼 이름과 일치하면 통과
   - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 던짐
4. 기존 동작(플랫폼 검사 생략)은 `platforms=None`일 때 그대로 유지