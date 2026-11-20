### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
      :param str filename: The name of the wheel file.
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.

      >>> from packaging.utils import parse_wheel_filename
=======
      :param str filename: The name of the wheel file.
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :param Iterable[str] | None platforms: An iterable of platform names to
          validate against, or ``None`` to skip platform validation.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>` or if none of the wheel's
          platform tags match the supplied *platforms*.

      >>> from packaging.utils import parse_wheel_filename
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
          normalized_platforms = frozenset(
              p.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
              for p in platforms
          )
          has_matching_platform = False
          for tag in tags:
              if tag.platform == "any":
                  has_matching_platform = True
                  break
              normalized_tag_platform = (
                  tag.platform.replace(".", "_").replace("-", "_").replace(" ", "_").lower()
              )
              if normalized_tag_platform in normalized_platforms:
                  has_matching_platform = True
                  break

          if not has_matching_platform:
              raise InvalidWheelFilename(
                  f"Invalid wheel filename (platform tag does not match requested platforms): {filename!r}"
              )

      return (name, version, build, tags)
>>>>>>> REPLACE