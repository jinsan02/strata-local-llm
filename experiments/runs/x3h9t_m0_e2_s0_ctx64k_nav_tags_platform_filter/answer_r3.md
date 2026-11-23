수정 내용을 요약하면:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
2. `typing.Iterable` 임포트 추가
3. `tags._normalize_string` 임포트 추가
4. 기존 검증(확장자, 이름, 버전, 빌드 번호, 태그)이 끝난 후 플랫폼 필터링 로직 추가:
   - `platforms`가 `str`이면 `TypeError`
   - 각 플랫폼 이름을 `_normalize_string(p).lower()`로 정규화 (`.`, `-`, ` ` → `_`, 소문자)
   - 태그 중 `platform == "any"`이거나 정규화된 이름 집합에 포함되면 통과
   - 하나도 없으면 `InvalidWheelFilename` 던짐
5. `platforms=None`일 때는 기존 동작과 동일하게 통과

기존 테스트 317개 모두 통과.