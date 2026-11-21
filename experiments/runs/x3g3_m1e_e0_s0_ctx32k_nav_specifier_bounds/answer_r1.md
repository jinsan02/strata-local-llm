### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
          # Empty SpecifierSet.
          return _apply_prereleases_filter(iterable, key, prereleases)
=======
          # Empty SpecifierSet.
          return _apply_prereleases_filter(iterable, key, prereleases)

    def bounds(self) -> tuple[
        tuple[Version, bool] | None, tuple[Version, bool] | None
    ]:
        """Return the lower and upper bounds of this specifier set.

        Returns a tuple ``(lower, upper)``, where each is ``None`` or a tuple
        ``(Version, inclusive: bool)``.

        >>> SpecifierSet(">=1.0,<2.0").bounds()
        ((<Version('1.0')>, True), (<Version('2.0')>, True))
        >>> SpecifierSet(">=1.0,<=1.0").bounds()
        ((<Version('1.0')>, True), (<Version('1.0')>, True))
        >>> SpecifierSet("==1.2.*").bounds()
        ((<Version('1.2')>, True), (<Version('1.3')>, False))
        >>> SpecifierSet("~=1.4.5").bounds()
        ((<Version('1.4.5')>, True), (<Version('1.5')>, False))
        >>> SpecifierSet("").bounds()
        (None, None)
        """
        if not self._specs:
            return (None, None)

        for spec in self._specs:
            if spec.operator == "===":
                raise ValueError("Cannot compute bounds for === specifiers")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver = spec._require_spec_version()
            ver_str = spec.version

            l: tuple[Version, bool] | None = None
            u: tuple[Version, bool] | None = None

            if op == ">=":
                l = (ver, True)
            elif op == ">":
                l = (ver, False)
            elif op == "<=":
                u = (ver, True)
            elif op == "<":
                u = (ver, False)
            elif op == "==":
                l = (ver, True)
                if ver_str.endswith(".*"):
                    release = ver._release
                    new_release = release[:-1] + (release[-1] + 1,)
                    upper_ver_str = f"{ver.epoch}!{'.'.join(map(str, new_release))}"
                    u = (Version(upper_ver_str), False)
                else:
                    u = (ver, True)
            elif op == "~=":
                l = (ver, True)
                release = ver._release
                if len(release) > 1:
                    new_release = release[:-2] + (release[-2] + 1,)
                else:
                    new_release = (release[0] + 1,)
                upper_ver_str = f"{ver.epoch}!{'.'.join(map(str, new_release))}"
                u = (Version(upper_ver_str), False)

            # Merge lower bounds: take the maximum, break ties with inclusive=False
            if l is not None:
                if lower is None:
                    lower = l
                else:
                    v1, inc1 = lower
                    v2, inc2 = l
                    if v2 > v1 or (v2 == v1 and not inc1):
                        lower = l
                    if v2 == v1:
                        lower = (v1, False)

            # Merge upper bounds: take the minimum, break ties with inclusive=False
            if u is not None:
                if upper is None:
                    upper = u
                else:
                    v1, inc1 = upper
                    v2, inc2 = u
                    if v2 < v1 or (v2 == v1 and not inc1):
                        upper = u
                    if v2 == v1:
                        upper = (v1, False)

        return (lower, upper)
>>>>>>> REPLACE