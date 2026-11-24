EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
        from .ranges import VersionRange  # noqa: PLC0415

        return VersionRange._from_specifier_set(self)

    def _check_relation_operand(self, other: object) -> None:
=======
        from .ranges import VersionRange  # noqa: PLC0415

        return VersionRange._from_specifier_set(self)

    def bounds(self) -> tuple[Version | None, bool] | tuple[None, None]:
        """Return the combined lower and upper bounds of the specifier set.

        Returns a tuple ``(lower, upper)`` where each element is either
        ``None`` (unbounded) or a ``(Version, inclusive)`` tuple.
        Raises ``ValueError`` if any specifier uses ``===``.
        """
        if not self._specs:
            return (None, None)

        if self._has_arbitrary:
            raise ValueError("=== specifiers are not supported by bounds()")

        lower_ver: Version | None = None
        lower_inc: bool = False
        upper_ver: Version | None = None
        upper_inc: bool = False

        first = True
        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            ver = spec._require_spec_version()

            lv: Version | None = None
            li: bool = False
            uv: Version | None = None
            ui: bool = False

            if op == ">=":
                lv, li = ver, True
            elif op == ">":
                lv, li = ver, False
            elif op == "<=":
                uv, ui = ver, True
            elif op == "<":
                uv, ui = ver, False
            elif op == "==":
                if ver_str.endswith(".*"):
                    lv, li = ver, True
                    new_rel = (*ver.release[:-1], ver.release[-1] + 1)
                    uv = Version.from_parts(epoch=ver.epoch, release=new_rel)
                    ui = False
                else:
                    lv, li = ver, True
                    uv, ui = ver, True
            elif op == "!=":
                pass
            elif op == "~=":
                lv, li = ver, True
                new_rel = (*ver.release[:-1], ver.release[-2] + 1)
                uv = Version.from_parts(epoch=ver.epoch, release=new_rel)
                ui = False
            else:
                raise ValueError(f"Unknown operator: {op}")

            if first:
                lower_ver, lower_inc, upper_ver, upper_inc = lv, li, uv, ui
                first = False
                continue

            if lv is not None:
                if lower_ver is None:
                    lower_ver, lower_inc = lv, li
                elif lv > lower_ver:
                    lower_ver, lower_inc = lv, li
                elif lv == lower_ver and not li:
                    lower_inc = False

            if uv is not None:
                if upper_ver is None:
                    upper_ver, upper_inc = uv, ui
                elif uv < upper_ver:
                    upper_ver, upper_inc = uv, ui
                elif uv == upper_ver and not ui:
                    upper_inc = False

        lower = (lower_ver, lower_inc) if lower_ver is not None else None
        upper = (upper_ver, upper_inc) if upper_ver is not None else None
        return (lower, upper)

    def _check_relation_operand(self, other: object) -> None:
>>>>>>> REPLACE