수정 완료 내용을 확인했습니다. 변경 사항 요약:

1. **`src/packaging/utils.py`**:
   - `typing.Iterable` import 추가
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `str`인 경우 `TypeError` 발생
   - 각 플랫폼 이름을 `_normalize_platform()` 로 정규화(`.` `- ` ` ` → `_`, 소문자) 후 비교
   - 태그 중 하나라도 플랫폼이 `"any"` 이거나 정규화된Platforms 집합에 포함되면 통과
   - 통과 실패 시 기존 예외와 같은 방식으로 `InvalidWheelFilename` 발생
   - 기존 동작(기존 검사 순서/메시지, 반환값)은 변경 없음
   - `_normalize_platform()` 헬퍼 함수 추가