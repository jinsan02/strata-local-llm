`src/packaging/utils.py` 파일에 다음 수정을 적용했습니다:

1. `typing.Iterable` 임포트 추가
2. `tags._normalize_string` 임포트 추가
3. `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
4. 태그 파싱 후, `platforms`가 `None`이 아닌 경우:
   - 인자가 문자열(`str`)이면 `TypeError` 발생
   - 주어진 플랫폼 이름들을 `_normalize_string`으로 정규화
   - 파싱된 태그 중 정규화된 플랫폼 목록과 일치하거나 플랫폼이 `any`인 태그가 하나라도 있으면 통과, 없으면 `InvalidWheelFilename` 발생

기존 동작은 변경되지 않으며, `platforms`가 `None`일 때나 빈 iterable일 때(단, `any` 태그가 있으면 통과) 기존과 동일하게 동작합니다.