<<<<<<< SEARCH
import re
from typing import TYPE_CHECKING, cast
=======
import functools
import re
from typing import TYPE_CHECKING, cast
>>>>>>> REPLACE

`src/packaging/markers.py`에 `Marker.referenced_extras()` 메서드와 내부 헬퍼 `_referenced_extras()`를 추가했습니다. `src/packaging/requirements.py`에 `Requirement.marker_extras` 속성을 추가하고 `functools` 임포트를 보충했습니다. 기존 문자열화, 비교, 해시, 평가 동작은 변경되지 않았습니다.