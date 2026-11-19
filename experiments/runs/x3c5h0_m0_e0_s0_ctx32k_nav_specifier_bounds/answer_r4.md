EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
           self._ranges = intersect_specifier_bounds(s._to_ranges() for s in self._specs)
           return self._ranges

       def is_unsatisfiable(self) -> bool:
=======
           self._ranges = intersect_specifier_bounds(s._to_ranges() for s in self._specs)
           return self._ranges

       def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
           """Compute the combined version bounds of this specifier set.

           Returns a ``(lower, upper)`` tuple where each element is either
           ``None`` (unbounded) or ``(version, inclusive: bool)``.
           Raises :exc:`ValueError` if any ``===`` specifier is present.
           """
           if self._has_arbitrary:
               raise ValueError("=== specifier is not supported by bounds()")

           lower: tuple[Version, bool] | None = None
           upper: tuple[Version, bool] | None = None

           def _merge_lower(a: tuple[Version, bool] | None, b: tuple[Version, bool]) -> tuple[Version, bool]:
               if a is None: return b
               if a[0] < b[0]: return b
               if b[0] < a[0]: return a
               return b if not b[1] else a

           def _merge_upper(a: tuple[Version, bool] | None, b: tuple[Version, bool]) -> tuple[Version, bool]:
               if a is None: return b
               if a[0] > b[0]: return b
               if b[0] > a[0]: return a
               return b if not b[1] else a

           for spec in self._specs:
               op, ver_str = spec.operator, spec.version
               v = coerce_version(ver_str.removesuffix(".*"))

               if op == ">=":
                   lower = _merge_lower(lower, (v, True))
               elif op == ">":
                   lower = _merge_lower(lower, (v, False))
               elif op == "<=":
                   upper = _merge_upper(upper, (v, True))
               elif op == "<":
                   upper = _merge_upper(upper, (v, False))
               elif op == "==":
                   if ver_str.endswith(".*"):
                       lower = _merge_lower(lower, (v, True))
                       rel = list(v.release)
                       rel[-1] += 1
                       up_ver = Version(f"{v.epoch}!{'.'.join(map(str, rel))}")
                       upper = _merge_upper(upper, (up_ver, False))
                   else:
                       lower = _merge_lower(lower, (v, True))
                       upper = _merge_upper(upper, (v, True))
               elif op == "~=":
                   lower = _merge_lower(lower, (v, True))
                   rel = list(v.release)
                   rel.pop()
                   rel[-1] += 1
                   up_ver = Version(f"{v.epoch}!{'.'.join(map(str, rel))}")
                   upper = _merge_upper(upper, (up_ver, False))

           return lower, upper

       def is_unsatisfiable(self) -> bool:
>>>>>>> REPLACE