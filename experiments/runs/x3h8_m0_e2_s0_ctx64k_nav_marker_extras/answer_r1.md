### 요구사항 확인

| 요구사항 | 반영 위치 | 상태 |
|---------|----------|------|
| `Marker.referenced_extras()` 메서드 | `src/packaging/markers.py:696-708` | ✅ |
| `extra == "x"`, `"x" == extra` 등 모든 비교 연산 처리 | `src/packaging/markers.py:444-450` | ✅ |
| `"x" in extras` / `"x" not in extras` 처리 | `src/packaging/markers.py:452-454` | ✅ |
| `and`/`or` 중첩 재귀 탐색 | `src/packaging/markers.py:430-439` | ✅ |
| `dependency_groups` 등 제외 (Variable.value 체크) | `src/packaging/markers.py:444-454` | ✅ |
| extra 미사용 마커 → 빈 `frozenset` | `src/packaging/markers.py:426-427` | ✅ |
| `&`·`\|` 합성 마커 지원 (`_markers` 트리 전체 탐색) | `src/packaging/markers.py:708` | ✅ |
| `Requirement.marker_extras` 속성 | `src/packaging/requirements.py:161-170` | ✅ |
| 마커 없으면 빈 `frozenset` | `src/packaging/requirements.py:168-169` | ✅ |
| 기존 테스트 7921개 통과 | 자동 검사 결과 | ✅ |

### 변경 내용 요약

1. **`src/packaging/markers.py`**:
   - `NormalizedName = str` 타입 별명 추가 (라인 62)
   - `_collect_referenced_extras()` / `_collect_referenced_extras_recursive()` 헬퍼 함수 추가 (라인 419-457)
   - `Marker.referenced_extras()` 메서드 추가 (라인 696-708)

2. **`src/packaging/requirements.py`**:
   - `Requirement.marker_extras` property 추가 (라인 161-170)