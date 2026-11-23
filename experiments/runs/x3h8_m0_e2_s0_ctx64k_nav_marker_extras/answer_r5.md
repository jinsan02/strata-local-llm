과제 요구사항을 확인했다:

1. **`Marker.referenced_extras() -> frozenset[NormalizedName]`** — `src/packaging/markers.py:741`
2. **`extra` 변수 비교 (`==`, `!=`, `in`, `not in`) 수집** — `src/packaging/markers.py:766-771`
3. **`extras` 변수 멤버십 (`in`, `not in`) 수집** — `src/packaging/markers.py:773-777`
4. **정규화된 이름 반환** — `canonicalize_name` 사용 (`src/packaging/markers.py:768, 771, 777`)
5. **`and`/`or` 및 괄호 중첩 처리** — 재귀 `_collect` 호출 (`src/packaging/markers.py:761-762`)
6. **`dependency_groups` 등 제외** — `extra`와 `extras`만 체크 (`src/packaging/markers.py:766, 769, 774`)
7. **extra 미사용 시 빈 `frozenset`** — `src/packaging/markers.py:782-784`
8. **`&`·`|` 합성 마커 지원** — `_markers` 구조 재귀 처리로 자동 지원
9. **`Requirement.marker_extras` property** — `src/packaging/requirements.py:314-325`
10. **마커 없으면 빈 `frozenset`** — `src/packaging/requirements.py:323-324`
11. **기존 동작 불변** — 기존 테스트 7921개 통과

모든 요구사항을 반영했으며, 수정한 파일은 `src/packaging/markers.py`와 `src/packaging/requirements.py` 두 파일뿐이다.