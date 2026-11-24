새 파일 `tests/test_y_canonicalize_version.py`를 생성했습니다. `canonicalize_version`의 현재 동작을 고정하는 pytest 테스트를 포함하며, 다음을 모두 다룹니다:
- 기본 동작 (`strip_trailing_zero=True`) 및 옵션 (`strip_trailing_zero=False`)
- `Version` 객체 입력 처리
- 유효하지 않은 버전 문자열은 원본 그대로 반환
- epoch, release, pre/post/dev, local 구성 요소별 처리
- 조합된 버전 문자열 및 `Version` 파싱과의 라운드트립 일관성

기존 코드에서 모두 통과하며, 향후 관련 함수나 `Version._trim_release` 등의 변경 시 실패하여 회귀를 감지하는 것이 목적입니다.