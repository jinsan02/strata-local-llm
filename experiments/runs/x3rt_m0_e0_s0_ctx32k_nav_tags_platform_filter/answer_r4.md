기존 테스트 317개 모두 통과했다.

수정 내용 요약:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `collections.abc.Iterable` import 추가
   - `_normalize_platform(str) → str` 헬퍼 함수 추가 (`.`·`-`·공백 → `_`, 소문자)
   - `platforms`가 `None`이 아니면: `str`이면 `TypeError`, 아니면 iterable의 각 항목을 정규화해 `frozenset`으로 만들고, 태그 중 `platform == "any"` 또는 정규화된 플랫폼 집합에 포함되면 통과, 아니면 `InvalidWheelFilename` 던짐