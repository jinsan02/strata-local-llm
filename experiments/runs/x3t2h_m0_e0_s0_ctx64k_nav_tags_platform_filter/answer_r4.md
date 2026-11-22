수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `typing.Iterable` import 추가
   - `tags._normalize_string` import 추가
   - `platforms` 가 `str` 이면 `TypeError` 던짐
   - `platforms` 가 `None` 이 아니면 각 플랫폼 이름을 `_normalize_string` 으로 정규화하여 `frozenset` 으로 저장
   - 기존 파싱 검사(확장자, 이름, 버전, 빌드번호, 태그) 통과 후 플랫폼 검증: 태그 중 `platform == "any"` 이거나 정규화된 플랫폼 이름과 일치하는 것이 있으면 통과, 아니면 `InvalidWheelFilename` 던짐
   - 기존 동작(`platforms=None`)은 완전히 동일하게 유지됨