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
    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    :param str filename: The name of the wheel file.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`.
=======
    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    If **platforms** is provided, the wheel's platform tags are checked
    against the given platform names. A wheel passes if any of its
    platform tags match one of the given platform names (normalized in the
    same way as :func:`packaging.tags._normalize_string`) or if the platform
    tag is ``"any"``. If no match is found, :class:`InvalidWheelFilename`
    is raised. If **platforms** is ``None``, no platform check is performed.

    :param str filename: The name of the wheel file.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :param Iterable[str] | None platforms: An iterable of platform name strings
        to match against the wheel's platform tags.
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`, or if **platforms** is given
        and no platform tag matches.
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
                f"platforms must be an iterable of strings, not str: {platforms!r}"
            )
        normalized_platforms = frozenset(
            p.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
            for p in platforms
        )
        if not any(
            tag.platform == "any" or tag.platform in normalized_platforms
            for tag in tags
        ):
            raise InvalidWheelFilename(
                f"Invalid wheel filename (no matching platform tag for "
                f"{normalized_platforms!r}): {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE