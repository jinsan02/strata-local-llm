`src/packaging/utils.py` 파일에 다음 사항을 수정했습니다:

1. `from collections.abc import Iterable` import 추가
2. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
3. 기존 파일명/태그 검증 완료 후, `platforms` 가 `None` 이 아닐 때 다음 로직 수행:
   - `platforms` 가 `str` 타입이면 `TypeError` 발생
   - 주어진 플랫폼 이름들을 `.`/`-`/` ` → `_` 치환 및 소문자 변환으로 정규화하여 집합화
   - 휠 태그 중 `platform == "any"` 인 것이 있거나, 정규화된 태그 플랫폼이 주어진 플랫폼 집합에 포함되면 통과
   - 조건을 만족하지 않으면 `InvalidWheelFilename` 발생
4. docstring 에 `platforms` 파라미터 설명 및 버전 변경 사항(`.. versionadded:: 26.4`) 추가

기존 `None` 전달 시 동작은 완전히 동일하게 유지되며, `validate_order` 파라미터와 함께 사용 가능합니다.