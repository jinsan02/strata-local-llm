EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
          return VersionRange._from_specifier_set(self)

    def _check_relation_operand(self, other: object) -> None:
=======
          return VersionRange._from_specifier_set(self)

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the combined lower and upper bounds of this specifier set.

        Returns a ``(lower, upper)`` tuple where each element is either ``None`` or
        a ``(version, inclusive)`` tuple. Empty sets return ``(None, None)``.
        If any specifier uses ``===``, raises :exc:`ValueError`.

        >>> SpecifierSet(">=1.0,!=2.0").bounds()
        ((<Version('1.0')>, True), None)
        >>> SpecifierSet("==1.2.*").bounds()
        ((<Version('1.2')>, True), (<Version('1.3')>, False))
        """
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            if spec.operator == "===":
                raise ValueError("=== operator does not support bounds calculation")

            op = spec.operator
            ver_str = spec.version
            v = Version(ver_str.removesuffix(".*"))

            l_new: tuple[Version, bool] | None = None
            u_new: tuple[Version, bool] | None = None

            if op in (">=", "==", "~="):
                l_new = (v, True)
            elif op == ">":
                l_new = (v, False)

            if op in ("<=", "=="):
                u_new = (v, True)
            elif op == "<":
                u_new = (v, False)
            elif op == "==" and ver_str.endswith(".*"):
                # Wildcard upper: increment last release digit, strip pre/post/dev/local
                rel = list(v.release)
                rel[-1] += 1
                upper_v = ".".join(map(str, rel))
                if v.epoch != 0:
                    upper_v = f"{v.epoch}!{upper_v}"
                u_new = (Version(upper_v), False)
            elif op == "~=":
                # ~= upper: drop last release part, increment new last part
                rel = list(v.release)
                if len(rel) > 1:
                    rel.pop()
                    rel[-1] += 1
                else:
                    rel[0] += 1
                upper_v = ".".join(map(str, rel))
                if v.epoch != 0:
                    upper_v = f"{v.epoch}!{upper_v}"
                u_new = (Version(upper_v), False)

            # Update lower bound
            if l_new is not None:
                if lower is None:
                    lower = l_new
                else:
                    c_v, c_inc = lower
                    n_v, n_inc = l_new
                    if n_v > c_v or (n_v == c_v and not n_inc):
                        lower = l_new

            # Update upper bound
            if u_new is not None:
                if upper is None:
                    upper = u_new
                else:
                    c_v, c_inc = upper
                    n_v, n_inc = u_new
                    if n_v < c_v or (n_v == c_v and not n_inc):
                        upper = u_new

        return lower, upper

    def _check_relation_operand(self, other: object) -> None:
>>>>>>> REPLACE