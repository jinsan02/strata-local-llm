<<<<<<< SEARCH
import re
from typing import NewType, cast
=======
import re
from collections.abc import Iterable
from typing import NewType, cast
>>>>>>> REPLACE

### 변경 내용 요약
- `src/packaging/utils.py`의 `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자를 추가했습니다.
- `platforms`가 `str`인 경우 즉시 `TypeError`를 던지는 검증 로직을 추가했습니다.
- `platforms`가 `None`이 아닌 경우, 제공된 플랫폼 이름들을 `packaging.tags`의 정규화 규칙(`.`/`-`/` ` → `_`, 소문자 변환)에 맞게 정규화한 후 집합으로 변환합니다. 이후 휠의 모든 태그 플랫폼 중 `any` 또는 정규화된 플랫폼 집합과 일치하는 것이 있는지 확인하고, 없으면 `InvalidWheelFilename`을 던집니다.
- `Iterable` 타입 힌트를 위해 `collections.abc`에서 `Iterable`을 import했습니다.
- `platforms=None`(기본값)일 때는 기존과 완전히 동일하게 동작하며, 기존 검사 순서와 반환값도 변경되지 않았습니다.