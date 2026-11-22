### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
import re
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, parse_tag
=======
import re
from collections.abc import Iterable
from typing import NewType, cast

from .tags import InvalidTag, Tag, UnsortedTagsError, _normalize_string, parse_tag
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
        # Reject bare str
        if isinstance(platforms, str):
            raise TypeError(
                f"platforms must be an iterable of strings, not str"
            )
        # Normalize the provided platform names once
        normalized_platforms = frozenset(
            _normalize_string(p) for p in platforms
        )
        # Check if any tag's platform matches
        found = False
        for tag in tags:
            if tag.platform == "any" or _normalize_string(tag.platform) in normalized_platforms:
                found = True
                break
        if not found:
            raise InvalidWheelFilename(
                f"Wheel platform(s) not compatible with given platforms: {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE