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
                "parse_wheel_filename() 'platforms' argument must be an iterable "
                "of strings, not a single string"
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
                f"Invalid wheel filename (platform tag(s) not compatible with "
                f"provided platforms): {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE