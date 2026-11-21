수정 사항을 요약하면:

1. **`src/packaging/utils.py`** 수정:
   - `from collections.abc import Iterable` 추가
   - `_normalize_platform_tag(platform: str) → str` 헬퍼 함수 추가: `.`, `-`, 공백을 `_`로 바꾸고 소문자로 변환 (PEP 625 / `packaging.tags` 규칙과 동일)
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
     - `None`이면 기존 동작과 동일
     - `str`을 직접 전달하면 `TypeError`
     - 주어진 플랫폼 이름들을 정규화한 집합과 wheel 태그의 플랫폼을 비교
     - 태그의 플랫폼이 `"any"`이면 모든 `platforms` (빈 iterable 포함) 에 통과
     - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 발생
     - 기존 파일명 검사 (확장자, 이름, 버전, 빌드번호, 태그) 가 먼저 실행되고 그 다음에 플랫폼 필터링