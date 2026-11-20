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
      :param platforms: An iterable of platform names to filter the wheel tags.
          If provided, the wheel must have at least one tag matching one of the
          provided platform names (after normalization). If not provided, no
          filtering is performed.
      :type platforms: collections.abc.Iterable[str] | None
      :raises InvalidWheelFilename: If the filename in question
          does not follow the :ref:`wheel specification
          <pypug:binary-distribution-format>`.
      :raises TypeError: If **platforms** is a string.

      >>> from packaging.utils import parse_wheel_filename
>>>>>>> REPLACE

`parse_wheel_filename` 함수에 `platforms` 키워드 전용 인자를 추가했습니다.
- `platforms`가 `None`이 아닌 경우 `str`인지 확인하여 `TypeError`를 던집니다.
- `platforms`의 각 항목과 태그의 플랫폼을 정규화(`.`/`-`/` ` → `_`, 소문자)하여 비교합니다.
- 태그 중 하나라도 `any`이거나 `platforms`와 일치하면 통과합니다.
- 일치하는 태그가 없으면 `InvalidWheelFilename`을 던집니다.
- docstring을 업데이트했습니다.