모든 요구사항 확인 완료:

- `Marker.referenced_extras()` 메서드: `src/packaging/markers.py:741-764` — `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 모두 처리, 정규화(`canonicalize_name`) 적용, `frozenset[NormalizedName]` 반환
- 중첩 식 처리: `src/packaging/markers.py:771-774` — 재귀적으로 `list`(괄호 중첩) 순회
- `dependency_groups` 등 다른 변수 무시: `src/packaging/markers.py:779-794` — `extra`/`extras` 변수만 필터링
- `&` · `|` 동작: 기존 `__and__`/`__or__`가 `_markers`를 조합하므로 `referenced_extras()`가 자동으로 처리
- `Requirement.marker_extras` 속성: `src/packaging/requirements.py:314-325` — 마커 없으면 `frozenset()`, 있으면 `marker.referenced_extras()`
- 기존 동작 변경 없음: 기존 메서드/속성 수정 안 함, 테스트 7921개 모두 통과

**변경 요약**:
- `src/packaging/markers.py`: `NormalizedName` import 추가, `Marker.referenced_extras()` 메서드 + `_collect_referenced_extras()` 정적 메서드 추가
- `src/packaging/requirements.py`: `NormalizedName` import 추가, `Requirement.marker_extras` property 추가