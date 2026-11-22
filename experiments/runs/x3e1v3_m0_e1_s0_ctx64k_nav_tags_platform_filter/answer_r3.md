`src/packaging/utils.py` 파일에 다음 내용을 수정했습니다:

1. `from collections.abc import Iterable` import 추가
2. 플랫폼 이름 정규화용 헬퍼 함수 `_normalize_platform` 추가
3. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가 및 docstring 갱신
4. 태그 파싱 완료 후, `platforms`가 `None`이 아닐 때 검증 로직 추가:
   - `str`을 전달하면 `TypeError` 발생
   - 전달된 플랫폼 목록을 정규화한 집합과 wheel의 태그 플랫폼 간 교집합이 비어있지 않으면 통과
   - 태그에 `any` 플랫폼이 포함되거나 교집합이 있으면 통과, 아니면 `InvalidWheelFilename` 발생