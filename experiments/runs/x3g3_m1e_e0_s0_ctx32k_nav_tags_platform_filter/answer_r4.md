`src/packaging/utils.py` 파일에 다음 수정을 적용했습니다:

1. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
2. 플랫폼 이름 정규화용 내부 헬퍼 `_normalize_platform` 함수 추가 (`.`, `-`, ` ` → `_` 치환 및 소문자화)
3. `platforms`가 `None`이 아닌 경우:
   - 인자가 `str`이면 `TypeError` 발생
   - iterable을 순회하며 정규화된 플랫폼 이름 집합 생성
   - wheel 태그 중 `platform == "any"`이거나 정규화 후 집합에 포함되면 통과, 아니면 `InvalidWheelFilename` 발생
4. 기존 검증 로직(확장자, 이름, 버전, 빌드 번호, 태그 파싱) 및 반환값은 변경 없음
5. docstring에 `platforms` 파라미터 및 `TypeError` 설명, 버전 추가 문단 반영