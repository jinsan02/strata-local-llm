`src/packaging/utils.py` 파일에 다음 내용을 수정했습니다.

1. `collections.abc.Iterable` import 추가.
2. 플랫폼 이름 정규화를 위한 `_normalize_platform` 헬퍼 함수 추가.
3. `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms` 추가 (기본값 `None`).
4. `platforms`가 `None`이 아닐 때, 주어진 iterable의 플랫폼 이름과 휠의 태그 플랫폼을 정규화하여 비교하는 로직 추가.
5. `platforms`가 `str`인 경우 `TypeError` 발생.
6. `any` 플랫폼 태그는 항상 통과.
7. 매칭되지 않으면 `InvalidWheelFilename` 발생.
8. 기존 동작(확장자, 이름, 버전 등 검사)은 유지되며 가장 마지막에 플랫폼 검사가 수행됨.