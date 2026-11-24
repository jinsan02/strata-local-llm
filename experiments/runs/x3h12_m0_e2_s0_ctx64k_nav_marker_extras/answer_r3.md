수정을 완료했습니다. 주요 변경 사항 요약:

- `src/packaging/markers.py`: `Marker` 클래스에 `referenced_extras()` 메서드와 내부 순회 헬퍼 `_collect_extras()`를 추가했습니다. `NormalizedName` 타입을 import했습니다.
- `src/packaging/requirements.py`: `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다. `NormalizedName` 타입을 import했습니다.

기존 문자열화, 비교, 해시, 평가 동작은 변경되지 않았습니다.