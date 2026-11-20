EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def to_range(self) -> ranges.VersionRange:
        """Return the :class:`~packaging.ranges.VersionRange` this set accepts.
=======
    def bounds(
        self,
    ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the combined lower and upper bounds of the specifier set.

        Returns a 2-tuple ``(lower, upper)`` where each element is either
        ``None`` (unbounded) or ``(version, inclusive: bool)``.

        >>> SpecifierSet(">=1.0,<2.0").bounds()
        (<Version('1.0')>, <Version('2.0')>)
        >>> SpecifierSet(">1.0,<2.0").bounds()
        ((<Version('1.0')>, False), (<Version('2.0')>, True))
        >>> SpecifierSet(">=1.4.5,~=1.4.5rc1").bounds()
        ((<Version('1.4.5rc1')>, True), (<Version('1.5')>, False))
        >>> SpecifierSet("").bounds()
        (None, None)
        >>> SpecifierSet("===1.0").bounds()
        Traceback (most recent call last):
            ...
        ValueError: Cannot compute bounds for SpecifierSet containing '===' operator.
        """
        if self._has_arbitrary:
            raise ValueError(
                "Cannot compute bounds for SpecifierSet containing '===' operator."
            )

        lower_ver: Version | None = None
        lower_inc: bool = False

        upper_ver: Version | None = None
        upper_inc: bool = False

        def _update_lower(ver: Version, inc: bool) -> None:
            nonlocal lower_ver, lower_inc
            if lower_ver is None or ver > lower_ver or (ver == lower_ver and not inc and lower_inc):
                lower_ver, lower_inc = ver, inc

        def _update_upper(ver: Version, inc: bool) -> None:
            nonlocal upper_ver, upper_inc
            if upper_ver is None or ver < upper_ver or (ver == upper_ver and not inc and upper_inc):
                upper_ver, upper_inc = ver, inc

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version

            v = spec._require_spec_version()

            if op == ">=":
                _update_lower(v, True)
            elif op == ">":
                _update_lower(v, False)
            elif op == "<=":
                _update_upper(v, True)
            elif op == "<":
                _update_upper(v, False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    _update_lower(v, True)
                    rel = v.release[:-1] if len(v.release) > 1 else ()
                    if rel:
                        rel = rel[:-1] + (rel[-1] + 1,)
                    else:
                        rel = (v.release[0] + 1,)
                    _update_upper(Version(f"{v.epoch}!{'.'.join(map(str, rel))}"), False)
                else:
                    _update_lower(v, True)
                    _update_upper(v, True)
            elif op == "~=":
                _update_lower(v, True)
                rel = v.release[:-1] if len(v.release) > 1 else ()
                if rel:
                    rel = rel[:-1] + (rel[-1] + 1,)
                else:
                    rel = (v.release[0] + 1,)
                _update_upper(Version(f"{v.epoch}!{'.'.join(map(str, rel))}"), False)
            # != gives no bounds

        lower_result = (lower_ver, lower_inc) if lower_ver is not None else None
        upper_result = (upper_ver, upper_inc) if upper_ver is not None else None
        return lower_result, upper_result

    def to_range(self) -> ranges.VersionRange:
        """Return the :class:`~packaging.ranges.VersionRange` this set accepts.
>>>>>>> REPLACE