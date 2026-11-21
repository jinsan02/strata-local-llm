수정 내용 요약:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
2. **`typing.Iterable` import** 추가
3. **`_normalize_string` import** (`packaging.tags`에서) — 플랫폼 이름 정규화에 사용
4. 함수 본문에 `platforms is not None`일 때 검증 로직 추가:
   - `str`을 전달하면 `TypeError` 던짐
   - `_normalize_string(p).lower()`로 정규화된 플랫폼 이름 집합 생성
   - 태그 중 `platform == "any"`이거나 정규화한 플랫폼 이름이 일치하면 통과, 아니면 `InvalidWheelFilename` 던짐
5. 기존 동작 (`platforms=None`) 은 변경 없음. 기존 filename 검사 → tag 파싱 → 플랫폼 검증 순서 유지.