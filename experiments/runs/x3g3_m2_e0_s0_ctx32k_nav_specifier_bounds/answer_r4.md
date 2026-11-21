### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
      def is_unsatisfiable(self) -> bool:
=======
      def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          """Return the (lower, upper) bounds of the specifier set.
          
          Returns a tuple (lower, upper) where each is either None (unbounded)
          or a tuple (version, inclusive).
          """
          lower: tuple[Version, bool] | None = None
          upper: tuple[Version, bool] | None = None
          
          for spec in self._specs:
              op, ver_str = spec._spec
              if op == "===":
                  raise ValueError("=== operator is not supported in bounds()")
              if op == "!=":
                  continue
                  
              ver = spec._get_spec_version()
              l, u = self._compute_spec_bounds(op, ver_str, ver)
              
              if l is not None:
                  if lower is None or l[0] > lower[0] or (l[0] == lower[0] and not l[1]):
                      lower = l
              if u is not None:
                  if upper is None or u[0] < upper[0] or (u[0] == upper[0] and not u[1]):
                      upper = u
                      
          return (lower, upper)

      def _compute_spec_bounds(
          self, op: str, ver_str: str, ver: Version
      ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          if op == ">=":
              return (ver, True), None
          if op == ">":
              return (ver, False), None
          if op == "<=":
              return None, (ver, True)
          if op == "<":
              return None, (ver, False)
          if op == "==":
              if ver_str.endswith(".*"):
                  release = (*ver.release[:-1], ver.release[-1] + 1)
                  upper_ver = Version.from_parts(epoch=ver.epoch, release=release)
                  return (ver, True), (upper_ver, False)
              return (ver, True), (ver, True)
          if op == "~=":
              prefix = ver.release[:-1]
              if prefix:
                  upper_release = (*prefix[:-1], prefix[-1] + 1)
              else:
                  upper_release = (ver.release[0] + 1,)
              upper_ver = Version.from_parts(epoch=ver.epoch, release=upper_release)
              return (ver, True), (upper_ver, False)
          return None, None

      def is_unsatisfiable(self) -> bool:
>>>>>>> REPLACE