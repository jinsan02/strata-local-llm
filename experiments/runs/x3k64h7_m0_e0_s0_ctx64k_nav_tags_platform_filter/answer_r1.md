`src/packaging/utils.py` 파일에 다음 사항을 수정했습니다:

1. `collections.abc.Iterable` 임포트 추가
2. `_normalize_platform(name: str) -> str` 헬퍼 함수 추가 (`.`/`-`/공백을 `_`로 변환 후 소문자화)
3. `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
4. 해당 인자에 대한 docstring 설명 및 `.. versionchanged::` 주석 업데이트
5. 기존 검사 완료 후, `platforms`가 `None`이 아닌 경우 플랫폼 매칭 검증 로직 추가
   - `str` 타입을 직접 전달하면 `TypeError` 발생
   - 제공된 플랫폼 iterable을 정규화하여 wheel 태그의 플랫폼과 비교
   - 태그에 `any`가 있거나 정규화된 플랫폼과 일치하면 통과, 그렇지 않으면 `InvalidWheelFilename` 발생
   - 빈 iterable이 주어지면 `any` 태그가 있는 경우만 통과

기존 동작은 `platforms=None`일 때 완전히 유지되며, `validate_order` 파라미터와 함께 사용해도 문제가 없습니다.