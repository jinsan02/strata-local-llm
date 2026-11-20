### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

---

수정 내용 요약:
- `src/packaging/markers.py`: `Marker` 클래스에 `referenced_extras()` 메서드 및 내부 순회/추출 헬퍼(`_collect_extras`, `_extract_extra`)를 추가했습니다. `NormalizedName` 타입을 import했습니다.
- `src/packaging/requirements.py`: `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다. 마커가 없으면 빈 `frozenset`, 있으면 해당 마커의 `referenced_extras()` 결과를 반환합니다. `NormalizedName` import도 함께 추가했습니다.
기존 문자열화, 비교, 해시, 평가 동작은 전혀 변경하지 않았습니다.