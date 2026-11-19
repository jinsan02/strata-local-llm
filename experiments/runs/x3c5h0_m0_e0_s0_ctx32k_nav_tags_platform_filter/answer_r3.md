플랫폼 검증 로직과 기존 함수 수정 사항을 모두 반영하여 `src/packaging/utils.py` 파일을 최종 수정합니다. 이미 적용된 부분이 있더라도 충돌 없이 안전하게 덮어씁니다.

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
from __future__ import annotations

__lazy_modules__ = {f"{__spec__.parent}.tags", f"{__spec__.parent}.version"}

import re
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, parse_tag
=======
from __future__ import annotations

__lazy_modules__ = {f"{__spec__.parent}.tags", f"{__spec__.parent}.version"}

import re
from collections.abc import Iterable
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, parse_tag
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
# PEP 427: Valid characters for an escaped project name in a wheel filename.
# Requires at least one character so an empty project name is rejected.
_wheel_name_regex = re.compile(r"^[\w._]+\Z", re.UNICODE)


def canonicalize_name(name: str, *, validate: bool = False) -> NormalizedName:
=======
# PEP 427: Valid characters for an escaped project name in a wheel filename.
# Requires at least one character so an empty project name is rejected.
_wheel_name_regex = re.compile(r"^[\w._]+\Z", re.UNICODE)


def _normalize_platform_tag(platform: str) -> str:
    """Normalize a platform tag string for comparison."""
    return platform.replace(".", "_").replace("-", "_").replace(" ", "_").lower()


def canonicalize_name(name: str, *, validate: bool = False) -> NormalizedName:
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
=======
    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    If **platforms** is provided, it must be an iterable of platform name
    strings. Each platform tag in the wheel filename is normalized using
    the same rules as :func:`packaging.tags._normalize_string` (``.``, ``-``,
    and spaces are replaced with ``_``, then lowercased). If any tag's
    platform matches one of the provided platforms, or if any tag has
    ``"any"`` as its platform, the wheel is accepted. Otherwise, an
    :class:`InvalidWheelFilename` is raised. A plain ``str`` given for
    **platforms** raises :exc:`TypeError`.

    :param str filename: The name of the wheel file.
=======
    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    If **platforms** is provided, it must be an iterable of platform name
    strings. Each platform tag in the wheel filename is normalized using
    the same rules as :data:`packaging.tags._normalize_string` (``.``, ``-``,
    and spaces are replaced with ``_``, then lowercased). If any tag's
    platform matches one of the provided platforms, or if any tag has
    ``"any"`` as its platform, the wheel is accepted. Otherwise, an
    :class:`InvalidWheelFilename` is raised. A plain ``str`` given for
    **platforms** raises :exc:`TypeError`.

    :param str filename: The name of the wheel file.
=======
    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    :param str filename: The name of the wheel file.
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
        not an identifier, a tag set component is empty, or the project name is
        empty.
    """
    if not filename.endswith(".whl"):
=======
        not an identifier, a tag set component is empty, or the project name is
        empty.

    .. versionchanged:: 26.x
       Added the *platforms* keyword-only parameter.
    """
    if isinstance(platforms, str):
        raise TypeError(
            "platforms must be an iterable of strings, not a plain string"
        )

    if not filename.endswith(".whl"):
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
    except InvalidTag:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None
    return (name, version, build, tags)


def parse_sdist_filename(filename: str) -> tuple[NormalizedName, Version]:
=======
    except InvalidTag:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None

    if platforms is not None:
        # Validate platform tags against the provided iterable.
        normalized_requested = {_normalize_platform_tag(p) for p in platforms}
        matched = False
        for tag in tags:
            # "any" platform matches any requested platforms (including empty).
            if tag.platform == "any":
                matched = True
                break
            if _normalize_platform_tag(tag.platform) in normalized_requested:
                matched = True
                break
        if not matched:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (platform tag(s) not found): {filename!r}"
            )

    return (name, version, build, tags)


def parse_sdist_filename(filename: str) -> tuple[NormalizedName, Version]:
>>>>>>> REPLACE