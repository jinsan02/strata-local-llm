수정을 완료했습니다. 변경 사항을 요약하면:

1. `from collections.abc import Iterable` import 추가
2. `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
3. `platforms`가 `str`인 경우 `TypeError` 발생
4. 주어진 플랫폼 이름들을 `.`·`-`·공백 → `_` 변환 + 소문자 정규화 후 비교
5. 태그 중 하나라도 플랫폼이 `"any"`이거나 정규화된 요청 플랫폼과 일치하면 통과
6. 통과하지 못하면 `InvalidWheelFilename` 발생
7. 기존 동작(기본값 `None`)은 변경 없음
8. docstring에 파라미터 설명 및 버전 정보 추가