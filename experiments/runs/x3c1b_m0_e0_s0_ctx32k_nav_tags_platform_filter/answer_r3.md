### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
from typing import NewType, cast
=======
from typing import Iterable, NewType, cast
>>>>>>> REPLACE
### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
         empty.
      """
=======
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
              raise TypeError("platforms argument must be an iterable of strings, not str")
          
          normalized_platforms = {
              p.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
              for p in platforms
          }
          
          passed = any(
              tag.platform == "any" or tag.platform in normalized_platforms
              for tag in tags
          )
          
          if not passed:
              raise InvalidWheelFilename(
                  f"Invalid wheel filename (platform mismatch): {filename!r}"
              )

      return (name, version, build, tags)
>>>>>>> REPLACE