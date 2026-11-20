`src/packaging/utils.py` 파일의 `parse_wheel_filename` 함수를 수정했습니다.

1. `collections.abc.Iterable` import 추가
2. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
3. `platforms`가 `None`이 아닌 경우:
   - `str`을 직접 전달하면 `TypeError` 발생
   - 주어진 플랫폼 이름들을 정규화(`.`/`-`/` ` → `_`, 소문자)하여 집합으로 변환
   - wheel 태그의 플랫폼 중 하나라도 정규화된 플랫폼과 일치하거나 `any`이면 통과
   - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 발생
4. 기존 동작(`platforms=None`)은 변경 없음
5. docstring 업데이트