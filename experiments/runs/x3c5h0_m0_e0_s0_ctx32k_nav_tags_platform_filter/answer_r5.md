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
      :param platforms: Optional iterable of platform names to filter by. If provided,
          only wheels whose tags include a matching platform will pass. Platform names
          are normalized by replacing ``.``, ``-``, and whitespace with ``_`` and
          lowercasing. A platform tag of ``"any"`` matches any platforms value (including
          an empty iterable). Passing a plain string raises ``TypeError``.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.
>>>>>>> REPLACE

### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None
    return (name, version, build, tags)
=======
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid tag component): {filename!r}"
        ) from None

    if platforms is not None:
        if isinstance(platforms, str):
            raise TypeError("platforms must be an iterable of strings, not a plain str")
        norm_platforms = frozenset(
            p.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
            for p in platforms
        )
        has_any = any(t.platform == "any" for t in tags)
        if not has_any and (not norm_platforms or not any(
            t.platform in norm_platforms for t in tags
        )):
            raise InvalidWheelFilename(
                f"Invalid wheel filename (no matching platform tag): {filename!r}"
            )

    return (name, version, build, tags)
>>>>>>> REPLACE