### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
      def _get_ranges(self) -> Sequence[Interval]:
          """Intersect all specifiers into a single sequence of version ranges.

          Empty when unsatisfiable. Callers must ensure ``self._specs``
          is non-empty.
          """
=======
      def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          """Return the overall lower and upper bounds enforced by the specifier set.

          Returns a tuple `(lower, upper)` where each element is either ``None``
          (unbounded) or a ``(version, inclusive)`` tuple.  ``===`` specifiers
          raise ``ValueError`` because they carry no version range semantics.
          Pre-release policies are ignored as requested.
          """
          lower: tuple[Version, bool] | None = None
          upper: tuple[Version, bool] | None = None

          for spec in self._specs:
              op = spec.operator
              ver_str = spec.version

              if op == "===":
                  raise ValueError("Cannot compute bounds for '===' specifier")

              base_ver_str = ver_str.removesuffix(".*")
              ver = Version(base_ver_str)

              if op in ("~=", "=="):
                  is_tilde = op == "~="
                  lower = SpecifierSet._merge_lower(lower, (ver, True))

                  # Compute upper bound version
                  rel = ver.release[:-1] if is_tilde else ver.release
                  # PEP 440 guarantees release has at least one digit for '*',
                  # and at least two digits for '~='.
                  new_rel = rel[:-1] + (rel[-1] + 1,)
                  upper_ver_str = (f"{ver.epoch}!{'.'.join(map(str, new_rel))}"
                                   if ver.epoch else ".".join(map(str, new_rel)))
                  upper = SpecifierSet._merge_upper(upper, (Version(upper_ver_str), False))

              elif op == ">=":
                  lower = SpecifierSet._merge_lower(lower, (ver, True))
              elif op == ">":
                  lower = SpecifierSet._merge_lower(lower, (ver, False))
              elif op == "<=":
                  upper = SpecifierSet._merge_upper(upper, (ver, True))
              elif op == "<":
                  upper = SpecifierSet._merge_upper(upper, (ver, False))
              # ``!=`` contributes no bounds

          return lower, upper

      @staticmethod
      def _merge_lower(current: tuple[Version, bool] | None, candidate: tuple[Version, bool]) -> tuple[Version, bool] | None:
          """Keep the larger lower bound; if equal, exclusive wins."""
          if current is None or current[0] < candidate[0]:
              return candidate
          if current[0] > candidate[0]:
              return current
          return (current[0], False)

      @staticmethod
      def _merge_upper(current: tuple[Version, bool] | None, candidate: tuple[Version, bool]) -> tuple[Version, bool] | None:
          """Keep the smaller upper bound; if equal, exclusive wins."""
          if current is None or current[0] > candidate[0]:
              return candidate
          if current[0] < candidate[0]:
              return current
          return (current[0], False)

      def _get_ranges(self) -> Sequence[Interval]:
          """Intersect all specifiers into a single sequence of version ranges.

          Empty when unsatisfiable. Callers must ensure ``self._specs``
          is non-empty.
          """
>>>>>>> REPLACE