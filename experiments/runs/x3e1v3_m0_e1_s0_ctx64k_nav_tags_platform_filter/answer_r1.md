### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
import re
from typing import NewType, cast
=======
import re
from collections.abc import Iterable
from typing import NewType, cast
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
=======
def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
    platforms: Iterable[str] | None = None,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
      :param str filename: The name of the wheel file.
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.
=======
      :param str filename: The name of the wheel file.
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :param platforms: An iterable of platform names to filter by. If ``None``,
          no platform filtering is performed. Each name is normalized by
          replacing ``.``, ``-``, and spaces with ``_`` and lowercasing.
          A platform tag of ``"any"`` matches any platform list, including an
          empty one.
      :type platforms: collections.abc.Iterable[str] | None
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.
      :raises TypeError: If **platforms** is a ``str``.
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
      .. versionchanged:: 26.3
         Raises :class:`InvalidWheelFilename` when an interpreter component is
         not an identifier, a tag set component is empty, or the project name is
         empty.
      """
=======
      .. versionchanged:: 26.3
         Raises :class:`InvalidWheelFilename` when an interpreter component is
         not an identifier, a tag set component is empty, or the project name is
         empty.

      .. versionadded:: 26.4
         The *platforms* parameter.
      """
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
      except InvalidTag:
          raise InvalidWheelFilename(
              f"Invalid wheel filename (invalid tag component): {filename!r}"
          ) from None
    return (name, version, build, tags)
=======
      except InvalidTag:
          raise InvalidWheelFilename(
              f"Invalid wheel filename (invalid tag component): {filename!r}"
          ) from None

      if platforms is not None:
          if isinstance(platforms, str):
              raise TypeError(
                  "platforms must be an iterable of strings, not str"
              )
          normalized_platforms = frozenset(
              p.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
              for p in platforms
          )
          has_match = False
          for tag in tags:
              if tag.platform == "any":
                  has_match = True
                  break
              if tag.platform in normalized_platforms:
                  has_match = True
                  break
          if not has_match:
              raise InvalidWheelFilename(
                  f"Wheel platform does not match any of "
                  f"the requested platforms: {normalized_platforms!r}"
              )

    return (name, version, build, tags)
>>>>>>> REPLACE

---

`parse_wheel_filename` 에 키워드 전용 인자 `platforms` 를 추가했습니다.
- `collections.abc.Iterable` import 를 추가했습니다.
- 시그니처에 `platforms: Iterable[str] | None = None` 을 추가하고 docstring 및 버전 노트를 갱신했습니다.
- 기존 파싱/검사가 끝난 후, `platforms` 가 `None` 이 아니면 사용자 입력을 정규화(`.`/`-`/` ` → `_`, 소문자)하여 `frozenset` 으로 만들고, 태그 중 `platform == "any"` 이거나 정규화된 목록과 일치하는 것이 있는지 확인합니다. 일치하지 않으면 `InvalidWheelFilename` 을, `str` 을 직접 전달하면 `TypeError` 를 던집니다.
- 기존 동작(파라미터 미전달 시)은 완전히 유지됩니다.