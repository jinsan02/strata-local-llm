모든 요구사항을 확인했다.

| 요구사항 | 반영 위치 | 상태 |
|---------|----------|------|
| 기본값 `None`, `None`이면 기존 동작 | `src/packaging/utils.py:207`, `325` | ✅ |
| `str` 직접 전달 시 `TypeError` | `src/packaging/utils.py:326-329` | ✅ |
| 정규화 규칙: `.`, `-`, 공백 → `_`, 소문자 | `src/packaging/utils.py:331`, `339-343` | ✅ |
| 태그 중 하나라도 매치하면 통과 | `src/packaging/utils.py:335-347` | ✅ |
| `any` 플랫폼 태그는 항상 통과 (빈 iterable 포함) | `src/packaging/utils.py:336-338` | ✅ |
| 실패 시 `InvalidWheelFilename` | `src/packaging/utils.py:349-351` | ✅ |
| 기존 검사 먼저, 오류 메시지 동일 | `src/packaging/utils.py:276-323` (변경 없음) | ✅ |
| 반환값 동일, `validate_order` 호환 | `src/packaging/utils.py:353` | ✅ |
| 기존 동작 변경 없음 | `src/packaging/utils.py:325` (None 체크) | ✅ |
| 기존 테스트 317개 통과 | 자동 검사 결과 | ✅ |

추가 수정 없이 완료.