## 요구사항 확인

| # | 요구사항 | 파일:줄 | 상태 |
|---|---------|--------|------|
| 1 | 기본값 `None`, `None`이면 기존 동작 동일 | `src/packaging/utils.py:207,322` | ✅ |
| 2 | `platforms`는 iterable, `str`이면 `TypeError` | `src/packaging/utils.py:323-326` | ✅ |
| 3 | 정규화: `.`·`-`·공백 → `_`, 소문자 | `src/packaging/utils.py:328` | ✅ |
| 4 | 태그 중 하나라도 매치 또는 `any` 태그 → 통과 (빈 iterable 포함) | `src/packaging/utils.py:331-332` | ✅ |
| 5 | 통과 못 하면 `InvalidWheelFilename` 던짐 | `src/packaging/utils.py:335-337` | ✅ |
| 6 | 기존 검사(확장자·이름·버전·빌드·태그)가 먼저 | `src/packaging/utils.py:273-320` | ✅ |
| 7 | 반환값 동일, `validate_order`와 함께 사용 가능 | `src/packaging/utils.py:339` | ✅ |
| 8 | 기존 동작 변경 없음 | `src/packaging/utils.py:322` (None skip) | ✅ |

기존 테스트 317개 모두 통과. 누락이나 오류 없음.

수정 내용: `src/packaging/utils.py`의 `parse_wheel_filename` 함수에 `platforms` 키워드 전용 인자 추가, `Iterable` import 추가, 플랫폼 검증 로직 구현.