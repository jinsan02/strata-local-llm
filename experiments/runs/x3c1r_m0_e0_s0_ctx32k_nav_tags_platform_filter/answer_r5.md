### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
import re
from typing import NewType, cast
=======
import re
from typing import Iterable, NewType, cast
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

      >>> from packaging.utils import parse_wheel_filename
=======
      :param str filename: The name of the wheel file.
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :param platforms: Acceptable platform tags, as an iterable of strings.
          If ``None`` (the default), no platform filtering is performed.
          Passing a plain string for this parameter raises ``TypeError``.

      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.

      >>> from packaging.utils import parse_wheel_filename
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
    except InvalidTag:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None
    return (name, version, build, tags)


def p
=======
    except InvalidTag:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None

    if platforms is not None:
        if isinstance(platforms, str):
            raise TypeError(
                "parse_wheel_filename() 'platforms' argument must be an iterable of strings"
            )

        def _normalize_platform(name: str) -> str:
            return name.replace(".", "_").replace("-", "_").replace(" ", "_").lower()

        target_platforms = {_normalize_platform(p) for p in platforms}

        matched = False
        for tag in tags:
            if tag.platform == "any":
                matched = True
                break
            if _normalize_platform(tag.platform) in target_platforms:
                matched = True
                break

        if not matched:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (platform mismatch): {filename!r}"
            )

    return (name, version, build, tags)


def p
>>>>>>> REPLACE