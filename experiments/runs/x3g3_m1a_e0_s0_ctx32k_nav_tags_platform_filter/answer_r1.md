### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
import re
from typing import NewType, cast
=======
from collections.abc import Iterable
import re
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
          no filtering is applied.
      :type platforms: collections.abc.Iterable[str] or None
      :raises TypeError: If *platforms* is a ``str``.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.
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
            raise TypeError("platforms must be an iterable of strings, not str")
        
        normalized_platforms = {
            p.replace('.', '_').replace('-', '_').replace(' ', '_').lower()
            for p in platforms
        }
        
        if not any(
            tag.platform == "any" or tag.platform in normalized_platforms
            for tag in tags
        ):
            raise InvalidWheelFilename(
                f"Invalid wheel filename (no matching platform tags): {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE