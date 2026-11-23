### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
import re
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, parse_tag
=======
import re
from collections.abc import Iterable
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, _normalize_platform, parse_tag
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

    If **platforms** is provided, the wheel's platform tags are validated
    against the given iterable of platform names. A wheel passes if any
    of its platform tags matches a normalized platform name from the
    iterable, or if the tag's platform is ``any``. A single string
    passed directly will raise :class:`TypeError`.

    :param str filename: The name of the wheel file.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :param Iterable[str] | None platforms: An iterable of platform names to
        validate against.
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`, or if the platform tags do not
        match any of the provided platform names.
    :raises TypeError: If *platforms* is passed as a single string.

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
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
    tag_str = parts[-1]
    try:
        tags = parse_tag(tag_str, validate_order=validate_order)
    except UnsortedTagsError:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (compressed tag set components must be in "
            f"sorted order per PEP 425): {filename!r}"
        ) from None
    except InvalidTag:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None
    return (name, version, build, tags)
=======
    tag_str = parts[-1]
    try:
        tags = parse_tag(tag_str, validate_order=validate_order)
    except UnsortedTagsError:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (compressed tag set components must be in "
            f"sorted order per PEP 425): {filename!r}"
        ) from None
    except InvalidTag:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None

    if platforms is not None:
        if isinstance(platforms, str):
            raise TypeError(
                "platforms must be an iterable of strings, not str"
            )
        normalized_platforms = {_normalize_platform(p) for p in platforms}
        if not any(
            tag.platform == "any" or _normalize_platform(tag.platform) in normalized_platforms
            for tag in tags
        ):
            raise InvalidWheelFilename(
                f"Invalid wheel filename (platform tags do not match any of the provided platforms): {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE

### 변경 내용 요약
1. `src/packaging/tags.py`: `_normalize_platform` 헬퍼 함수 추가 (`.` `-` ` ` → `_` 변환 및 소문자화).
2. `src/packaging/utils.py`: 
   - `collections.abc.Iterable` 및 `_normalize_platform` import 추가.
   - `parse_wheel_filename` 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가.
   - docstring에 `platforms` 파라미터 설명 및 `TypeError`/`InvalidWheelFilename` 예외 문서화.
   - 태그 파싱 후 `platforms` 검증 로직 추가: `str` 직접 전달 시 `TypeError`, 정규화 후 매칭 실패 시 `InvalidWheelFilename` 발생. `any` 플랫폼 태그는 항상 통과. 기존 동작은 `platforms=None`일 때 동일하게 유지.