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
          :param platforms: An iterable of platform names to check against the wheel's tags.
              If ``None``, no platform check is performed. Platform names are normalized
              by replacing ``.``, ``-``, and spaces with ``_``, and lowercased.
              Passing a single string raises ``TypeError``.
          :raises InvalidWheelFilename: If the filename in question
              does not follow the :ref:`wheel specification
              <pypug:binary-distribution-format>`, or if the wheel's platform tags
              do not match the provided *platforms*.
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
              raise TypeError("platforms must be an iterable of strings, not a single string")
          
          # Normalize provided platforms using the same rule as packaging.tags
          normalized_platforms = frozenset(
              p.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
              for p in platforms
          )
          
          # Check if any tag matches the normalized platforms
          match_found = False
          for tag in tags:
              if tag.platform == "any":
                  match_found = True
                  break
              # Normalize tag platform for comparison (though usually already normalized)
              normalized_tag_platform = tag.platform.replace(".", "_").replace("-", "_").lower()
              if normalized_tag_platform in normalized_platforms:
                  match_found = True
                  break
          
          if not match_found:
              raise InvalidWheelFilename(
                  f"Invalid wheel filename (platform mismatch): {filename!r}"
              )

      return (name, version, build, tags)
>>>>>>> REPLACE