`src/packaging/utils.py`에서 `parse_wheel_filename` 함수를 다음과 같이 수정했습니다:

1.  **Import 추가**: `from collections.abc import Iterable`를 임포트하여 타입 힌트에 사용했습니다.
2.  **시그니처 변경**: 키워드 전용 인자 `platforms: Iterable[str] | None = None`을 추가했습니다.
3.  **문서화 (Docstring)**: `platforms` 파라미터의 역할, 정규화 규칙(`.`·`-`·공백을 `_`로 변경 및 소문자), `"any"` 플랫폼 처리, plain `str` 전달 시 `TypeError` 발생 사항 등을 설명하는 주석을 추가했습니다.
4.  **검증 로직 추가**: 태그 파싱 완료 후, `platforms`가 `None`이 아니면 제공된 문자열들을 지정된 규칙으로 정규화하여 집합을 만들고, 태그 중 하나라도 `"any"`이거나 정규화된 플랫폼과 일치하는지 검사합니다. 일치하지 않으면 `InvalidWheelFilename("Invalid wheel filename (incompatible platform tags): ...")`을 던집니다. 또한 입력이 평문 `str`인 경우 명시적으로 `TypeError`를.raise 합니다.

기존 테스트 파일은 수정하지 않았으며, 기존 동작(`platforms=None`)은 완전히 호환됩니다.