### EDIT: src/packaging/utils.py
<<<<<<< SEARCH
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.

      >>> from packaging.utils import parse_wheel_filename
=======
      :param bool validate_order: Check whether compressed tag set components
          are in sorted order.
      :param iterable platforms: An iterable of platform name strings to check
          against the wheel's platform tags. If provided, only wheels whose
          platform tags match one of the given names (or ``"any"``) are accepted.
          Platform names are normalized by replacing ``.``, ``-``, and spaces
          with ``_`` and lowercasing. If not provided (``None``), no platform
          filtering is performed.
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.

      >>> from packaging.utils import parse_wheel_filename
>>>>>>> REPLACE