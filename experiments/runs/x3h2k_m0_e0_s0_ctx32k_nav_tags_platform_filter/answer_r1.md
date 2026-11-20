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
    :param platforms: An iterable of platform names to filter the wheel tags.
        If provided, the wheel must have at least one tag whose platform matches
        one of the normalized platform names, or the tag's platform is "any".
        If ``None`` (default), no platform filtering is performed.
    :raises TypeError: If ``platforms`` is a string.
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`, or if the wheel's tags do not match
        the specified platforms.
>>>>>>> REPLACE

`parse_wheel_filename` 함수에 `platforms` 키워드 전용 인자를 추가하고, 해당 인자를 기반으로 휠 태그의 플랫폼을 검증하는 로직을 구현했습니다.
- `platforms` 인자는 `Iterable[str] | None` 타입이며, 기본값은 `None`입니다.
- `platforms`가 `str`인 경우 `TypeError`를 던집니다.
- `platforms`가 제공되면, 각 플랫폼 이름을 정규화(`.` `-` ` ` → `_`, 소문자)하여 비교합니다.
- 휠 태그 중 정규화된 플랫폼 이름과 일치하는 것이 있거나, 플랫폼이 `any`인 태그가 있으면 통과합니다.
- 일치하는 태그가 없으면 `InvalidWheelFilename`을 던집니다.
- 기존 동작(기본값 `None`)은 변경되지 않습니다.