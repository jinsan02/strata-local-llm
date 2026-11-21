### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
  _normalized_regex = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*", re.ASCII)
  # PEP 427: The build number must start with a digit.
=======
  _normalized_regex = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*", re.ASCII)
  # PEP 427: The build number must start with a digit.
  def _normalize_platform(platform: str) -> str:
      return platform.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
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
        normalized_platforms = frozenset(
            _normalize_platform(p) for p in platforms
        )
        if not any(
            tag.platform == "any" or _normalize_platform(tag.platform) in normalized_platforms
            for tag in tags
        ):
            raise InvalidWheelFilename(
                f"Invalid wheel filename (platform tags do not match "
                f"any of the specified platforms): {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE