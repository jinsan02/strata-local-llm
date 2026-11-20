EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def _get_ranges(self) -> Sequence[Interval]:
        """Intersect all specifiers into a single sequence of version ranges.

        Empty when unsatisfiable. Callers must ensure ``self._specs``
        is non-empty.
        """
        if self._ranges is not None:
            return self._ranges

        self._ranges = intersect_specifier_bounds(s._to_ranges() for s in self._specs)
        return self._ranges

    def is_unsatisfiable(self) -> bool:
=======
    def _get_ranges(self) -> Sequence[Interval]:
        """Intersect all specifiers into a single sequence of version ranges.

        Empty when unsatisfiable. Callers must ensure ``self._specs``
        is non-empty.
        """
        if self._ranges is not None:
            return self._ranges

        self._ranges = intersect_specifier_bounds(s._to_ranges() for s in self._specs)
        return self._ranges

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the implicit lower and upper bounds of this specifier set.

        Returns a ``(lower, upper)`` tuple where each bound is either ``None``
        (unbounded) or ``(version, inclusive)``.

        Raises :exc:`ValueError` if any specifier uses the identity operator ``===``.
        """
        if not self._specs:
            return (None, None)

        if any(s.operator == "===" for s in self._specs):
            raise ValueError("Bounds calculation does not support === specifiers")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        def _update_lower(v: Version, inc: bool) -> None:
            nonlocal lower
            if lower is None:
                lower = (v, inc)
            else:
                cv, ci = lower
                if v > cv or (v == cv and not inc and ci):
                    lower = (v, inc)

        def _update_upper(v: Version, inc: bool) -> None:
            nonlocal upper
            if upper is None:
                upper = (v, inc)
            else:
                cv, ci = upper
                if v < cv or (v == cv and not inc and ci):
                    upper = (v, inc)

        for spec in self._specs:
            op, ver_str = spec._spec
            version = spec._require_spec_version()

            if op == ">=":
                _update_lower(version, True)
            elif op == ">":
                _update_lower(version, False)
            elif op == "<=":
                _update_upper(version, True)
            elif op == "<":
                _update_upper(version, False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    _update_lower(version, True)
                    new_release = list(version.release[:-1]) + [version.release[-1] + 1]
                    epoch_str = f"{version.epoch}!" if version.epoch else ""
                    upper_ver = Version(f"{epoch_str}{'.'.join(str(r) for r in new_release)}")
                    _update_upper(upper_ver, False)
                else:
                    _update_lower(version, True)
                    _update_upper(version, True)
            elif op == "~=":
                _update_lower(version, True)
                rel = version.release
                if len(rel) >= 2:
                    new_release = list(rel[:-2]) + [rel[-2] + 1]
                else:
                    new_release = [rel[0]]
                epoch_str = f"{version.epoch}!" if version.epoch else ""
                upper_ver = Version(f"{epoch_str}{'.'.join(str(r) for r in new_release)}")
                _update_upper(upper_ver, False)
            elif op == "!=":
                pass

        return lower, upper

    def is_unsatisfiable(self) -> bool:
>>>>>>> REPLACE