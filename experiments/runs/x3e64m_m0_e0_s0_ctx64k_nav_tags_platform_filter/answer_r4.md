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
    return platform.replace(".", "_").replace("-", "_").replace(" ", "_").lower()


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
    :param Iterable[str] | None platforms: Platform names to validate against.
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`, or if **platforms** is
        given and no tag's platform matches any of the supplied names.
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
                f"platforms must be an iterable of strings, not str"
            )
        normalized_platforms = {
            _normalize_platform(p) for p in platforms
        }
        if not any(
            t.platform == "any" or t.platform in normalized_platforms
            for t in tags
        ):
            raise InvalidWheelFilename(
                f"Wheel platform(s) not in {normalized_platforms!r}: {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE