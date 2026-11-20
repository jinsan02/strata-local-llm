### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
from typing import NewType, cast
=======
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
def _normalize_platform(platform: str) -> str:
    """Normalize a platform name for comparison."""
    return re.sub(r"[\s.\-]", "_", platform).lower()


def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
    platforms: Iterable[str] | None = None,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.

      >>> from packaging.utils import parse_wheel_filename
=======
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :param platforms: An iterable of platform names to filter by. If given,
          only wheels whose tags contain a matching platform will pass.
          Platform names are normalized by replacing `.`, `-`, and whitespace
          with `_` and lowercasing. A platform tag of ``any`` matches any
          platforms value (including an empty iterable). If ``None``, no
          filtering is performed.
      :raises TypeError: If *platforms* is a plain string.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`, or if none of the wheel's
          platform tags match any name in *platforms*.

      >>> from packaging.utils import parse_wheel_filename
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
                "platforms must be an iterable of strings, not a plain string"
            )
        normalized_targets = {_normalize_platform(p) for p in platforms}
        matched = False
        for tag in tags:
            if tag.platform == "any" or _normalize_platform(tag.platform) in normalized_targets:
                matched = True
                break
        if not matched:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (platforms do not match): {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE