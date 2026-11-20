EDIT: src/packaging/utils.py
<<<<<<< SEARCH
def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
=======
def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
    platforms: Iterable[str] | None = None,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
>>>>>>> REPLACE

EDIT: src/packaging/utils.py
<<<<<<< SEARCH
        .. versionchanged:: 26.3
           Raises :class:`InvalidWheelFilename` when an interpreter component is
           not an identifier, a tag set component is empty, or the project name is
           empty.
        """
=======
        .. versionchanged:: 26.3
           Raises :class:`InvalidWheelFilename` when an interpreter component is
           not an identifier, a tag set component is empty, or the project name is
           empty.

        .. versionadded:: 26.4
           The *platforms* parameter.
        """
>>>>>>> REPLACE

EDIT: src/packaging/utils.py
<<<<<<< SEARCH
            ) from None
        return (name, version, build, tags)


def parse_sdist_filename(filename: str) -> tuple[NormalizedName, Version]:
=======
            ) from None
        
        if platforms is not None:
            if isinstance(platforms, str):
                raise TypeError(
                    f"platforms must be an iterable of strings, got {type(platforms).__name__!r}"
                )
            
            normalized_platforms = set()
            for plat in platforms:
                # Normalize platform name (replace separators with _, lowercase)
                norm_plat = str(plat).replace(".", "_").replace("-", "_").replace(" ", "_").lower()
                normalized_platforms.add(norm_plat)

            match_found = False
            for tag in tags:
                if tag.platform == "any":
                    match_found = True
                    break
                
                # Normalize wheel's platform to compare with provided platforms
                norm_tag_plat = str(tag.platform).replace(".", "_").replace("-", "_").replace(" ", "_")
                
                if norm_tag_plat in normalized_platforms:
                    match_found = True
                    break
            
            if not match_found:
                raise InvalidWheelFilename(
                    f"Invalid wheel filename (platform mismatch): {filename!r}"
                )

        return (name, version, build, tags)


def parse_sdist_filename(filename: str) -> tuple[NormalizedName, Version]:
>>>>>>> REPLACE