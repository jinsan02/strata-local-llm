### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
import re
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, parse_tag
=======
import re
from collections.abc import Iterable
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, parse_tag
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
    """
    This function takes the filename of a wheel file, and parses it,
    returning a tuple of name, version, build number, and tags.

    The name part of the tuple is normalized and typed as
    :class:`NormalizedName`. The version portion is an instance of
    :class:`~packaging.version.Version`. The build number is ``()`` if
    there is no build number in the wheel filename, otherwise a
    two-item tuple of an integer for the leading digits and
    a string for the rest of the build number. The tags portion is a
    frozen set of :class:`~packaging.tags.Tag` instances (as the tag
    string format allows multiple tags to be combined into a single
    string).

    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    :param str filename: The name of the wheel file.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`.

    >>> from packaging.utils import parse_wheel_filename
    >>> from packaging.tags import Tag
    >>> from packaging.version import Version
    >>> name, ver, build, tags = parse_wheel_filename("foo-1.0-py3-none-any.whl")
    >>> name
    'foo'
    >>> ver == Version('1.0')
    True
    >>> tags == {Tag("py3", "none", "any")}
    True
    >>> not build
    True

    .. versionadded:: 20.9

    .. versionchanged:: 23.2
       Raises :class:`InvalidWheelFilename` when the version component is invalid.

    .. versionadded:: 26.1
       The *validate_order* parameter.

    .. versionchanged:: 26.3
       Raises :class:`InvalidWheelFilename` when an interpreter component is
       not an identifier, a tag set component is empty, or the project name is
       empty.
    """
=======
def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
    platforms: Iterable[str] | None = None,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
    """
    This function takes the filename of a wheel file, and parses it,
    returning a tuple of name, version, build number, and tags.

    The name part of the tuple is normalized and typed as
    :class:`NormalizedName`. The version portion is an instance of
    :class:`~packaging.version.Version`. The build number is ``()`` if
    there is no build number in the wheel filename, otherwise a
    two-item tuple of an integer for the leading digits and
    a string for the rest of the build number. The tags portion is a
    frozen set of :class:`~packaging.tags.Tag` instances (as the tag
    string format allows multiple tags to be combined into a single
    string).

    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    If **platforms** is specified and not ``None``, the platform tag(s) of
    the wheel must match at least one of the given platform names (after
    normalization: ``.``, ``-``, and space are replaced with ``_`` and the
    result is lowercased). A wheel whose platform is ``any`` always passes.
    Passing a single ``str`` as **platforms** raises :class:`TypeError`.

    :param str filename: The name of the wheel file.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :param platforms: An iterable of platform name strings to match against.
    :type platforms: collections.abc.Iterable[str] or None
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`, or if the wheel's platform tags
        do not match any of the given **platforms**.

    >>> from packaging.utils import parse_wheel_filename
    >>> from packaging.tags import Tag
    >>> from packaging.version import Version
    >>> name, ver, build, tags = parse_wheel_filename("foo-1.0-py3-none-any.whl")
    >>> name
    'foo'
    >>> ver == Version('1.0')
    True
    >>> tags == {Tag("py3", "none", "any")}
    True
    >>> not build
    True

    .. versionadded:: 20.9

    .. versionchanged:: 23.2
       Raises :class:`InvalidWheelFilename` when the version component is invalid.

    .. versionadded:: 26.1
       The *validate_order* parameter.

    .. versionchanged:: 26.3
       Raises :class:`InvalidWheelFilename` when an interpreter component is
       not an identifier, a tag set component is empty, or the project name is
       empty.

    .. versionadded:: XX.YY
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


def parse_sdist_filename(filename: str) -> tuple[NormalizedName, Version]:
=======
    except InvalidTag:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None

    if platforms is not None:
        if isinstance(platforms, str):
            raise TypeError("platforms must be an iterable of strings, not a single string")
        normalized_plats = {
            p.replace(".", "_").replace("-", "_").replace(" ", "_").lower() for p in platforms
        }
        matched = False
        for tag in tags:
            if tag.platform == "any":
                matched = True
                break
            if (
                tag.platform.replace(".", "_").replace("-", "_").replace(" ", "_")
                in normalized_plats
            ):
                matched = True
                break
        if not matched:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (platform tags do not match any of the given platforms: {filename!r})"
            )

    return (name, version, build, tags)


def parse_sdist_filename(filename: str) -> tuple[NormalizedName, Version]:
>>>>>>> REPLACE

`packaging.utils.parse_wheel_filename` 함수에 `platforms` 키워드 전용 인자를 추가하고, 기본값이 `None`이 아닐 때 주어진 플랫폼 이름 iterable와 휠 태그의 플랫폼을 정규화하여 비교하는 검증 로직을 구현했습니다. 단일 문자열을 전달할 경우 `TypeError`를 발생시키며, 플랫폼이 `any`인 경우 항상 통과합니다. 기존 테스트 파일은 수정하지 않았습니다.