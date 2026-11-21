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
          allowed = {_normalize_platform_tag(p) for p in platforms}
          tag_platforms = {tag.platform for tag in tags}
          if not any(
              tp == "any" or tp in allowed for tp in tag_platforms
          ):
              raise InvalidWheelFilename(
                  f"Wheel is incompatible with any of {list(allowed)!r}"
              )

      return (name, version, build, tags)
>>>>>>> REPLACE