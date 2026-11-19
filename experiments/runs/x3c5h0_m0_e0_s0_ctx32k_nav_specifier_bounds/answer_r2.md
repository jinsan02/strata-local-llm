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
        """Return the combined lower and upper bounds of this specifier set.

        Returns a ``(lower, upper)`` tuple where each is either ``None`` or a
        ``(version, inclusive)`` pair. Bounds are intersected across all specifiers:
        the lowest bound wins for the lower limit, the highest for the upper limit.
        Raises :exc:`ValueError` if any specifier uses the ``===`` operator.
        """
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        if not self._specs:
            return (None, None)

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version

            if op == "===":
                raise ValueError("=== cannot be converted to bounds")

            is_wildcard = ver_str.endswith(".*")
            ver = Version(ver_str.removesuffix(".*"))

            s_lower: tuple[Version, bool] | None = None
            s_upper: tuple[Version, bool] | None = None

            if op == ">=":
                s_lower = (ver, True)
            elif op == ">":
                s_lower = (ver, False)
            elif op == "<=":
                s_upper = (ver, True)
            elif op == "<":
                s_upper = (ver, False)
            elif op == "==":
                if is_wildcard:
                    s_lower = (ver, True)
                    rel = list(ver.release)
                    rel[-1] += 1
                    s_upper = (Version.from_parts(epoch=ver.epoch, release=tuple(rel), dev=None), False)
                else:
                    s_lower = (ver, True)
                    s_upper = (ver, True)
            elif op == "~=":
                if len(ver.release) < 2:
                    raise ValueError("~= requires at least two release segments")
                s_lower = (ver, True)
                prefix_release = ver.release[:-1]
                next_rel = list(prefix_release)
                next_rel[-1] += 1
                s_upper = (Version.from_parts(epoch=ver.epoch, release=tuple(next_rel), dev=None), False)
            elif op == "!=":
                pass
            else:
                raise ValueError(f"Unknown operator: {op!r}")

            # Intersect lower bound (largest wins; exclusive beats inclusive at same version)
            if s_lower is not None:
                if lower is None:
                    lower = s_lower
                else:
                    v1, inc1 = lower
                    v2, inc2 = s_lower
                    if v2 > v1 or (v2 == v1 and not inc2):
                        lower = s_lower

            # Intersect upper bound (smallest wins; exclusive beats inclusive at same version)
            if s_upper is not None:
                if upper is None:
                    upper = s_upper
                else:
                    v1, inc1 = upper
                    v2, inc2 = s_upper
                    if v2 < v1 or (v2 == v1 and not inc2):
                        upper = s_upper

        return (lower, upper)

    def is_unsatisfiable(self) -> bool:
>>>>>>> REPLACE