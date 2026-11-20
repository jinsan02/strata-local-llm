### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :raises InvalidWheelFilename: If the filename in question
=======
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :param Iterable[str] | None platforms: Iterable of platform names to match
          against, or ``None`` to skip platform validation.
      :raises InvalidWheelFilename: If the filename in question
>>>>>>> REPLACE