### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
      def _check_relation_operand(self, other: object) -> None:
          if not isinstance(other, SpecifierSet):
              raise TypeError("expected a SpecifierSet")
          if self._has_arbitrary or other._has_arbitrary:
              raise ValueError("set relations do not support === specifiers")

      def is_subset(self, other: SpecifierSet) -> bool:
=======
      @staticmethod
      def _get_spec_bounds(spec):
          """Return the (lower_bound, upper_bound) tuple for a single specifier."""
          op = spec.operator
          version = spec._require_spec_version()

          if op in (">=", ">"):
              # lower = (V, inclusive)
              return ((version, op == ">="), None)
          
          if op in ("<=", "<"):
              # upper = (V, inclusive)
              return (None, (version, op == "<="))
          
          if op == "==":
              ver_str = spec.version
              if ver_str.endswith(".*"):
                  # Wildcard: lower=(V, True), upper=next_prefix(V, False)
                  release = version.release
                  new_release = (*release[:-1], release[-1] + 1)
                  next_ver = Version.from_parts(epoch=version.epoch, release=new_release)
                  return ((version, True), (next_ver, False))
              else:
                  # Exact: lower=(V, True), upper=(V, True) -> point
                  return ((version, True), (version, True))

          if op == "~=":
              # Compatible release: lower=(V, True), upper=next_prefix(V, False)
              release = version.release
              # Release without the last digit
              trimmed_release = release[:-1]
              if not trimmed_release:
                  trimmed_release = (0,)
              # Last digit increased by 1
              new_release = (*trimmed_release, trimmed_release[-1] + 1)
              next_ver = Version.from_parts(epoch=version.epoch, release=new_release)
              return ((version, True), (next_ver, False))

          # !=, === etc. do not contribute bounds
          return (None, None)

      @staticmethod
      def _compare_bounds(b1, b2):
          """Compare two bounds: returns True if b1 is 'greater' than b2 (or equal).
          
          For lower bounds: greater means more restrictive (larger version or same version with inclusive=False).
          For upper bounds: smaller means more restrictive (smaller version).
          Used internally to filter.
          """
          pass

      def _get_range_bounds(self):
          """Calculate the effective (lower, upper) bounds for this SpecifierSet."""
          if self._has_arbitrary:
              raise ValueError("bounds() does not support === specifiers")
          
          global_lower = None
          global_upper = None

          for spec in self._specs:
              lower, upper = self._get_spec_bounds(spec)

              # Merge lower bounds
              if lower is not None:
                  if global_lower is None:
                      global_lower = lower
                  else:
                      gl_ver, gl_inc = global_lower
                      l_ver, l_inc = lower
                      
                      if gl_ver == l_ver:
                          # Same version, inclusive=False takes precedence (is tighter start)
                          if not l_inc:
                              global_lower = (gl_ver, False)
                          # else: gl is already the best (inclusive=True or both False)
                      elif l_ver > gl_ver:
                          global_lower = lower
                      # If gl_ver > l_ver, keep gl

              # Merge upper bounds
              if upper is not None:
                  if global_upper is None:
                      global_upper = upper
                  else:
                      gu_ver, gu_inc = global_upper
                      u_ver, u_inc = upper
                      
                      if gu_ver == u_ver:
                          pass # Same version, keep existing
                      elif u_ver < gu_ver:
                          global_upper = upper
                      # If gu_ver < u_ver, keep gu

          return (global_lower, global_upper)

      def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          """Return the effective range bounds of this SpecifierSet.
          
        - Returns `(lower, upper)` tuple where each is either `None` or `(Version, inclusive: bool)`.
        - `ValueError` is raised if the set contains any `===` specifier.
        - Prerelease settings do not affect the returned bounds.
          """
          return self._get_range_bounds()

      def _check_relation_operand(self, other: object) -> None:
          if not isinstance(other, SpecifierSet):
              raise TypeError("expected a SpecifierSet")
          if self._has_arbitrary or other._has_arbitrary:
              raise ValueError("set relations do not support === specifiers")

      def is_subset(self, other: SpecifierSet) -> bool:
>>>>>>> REPLACE