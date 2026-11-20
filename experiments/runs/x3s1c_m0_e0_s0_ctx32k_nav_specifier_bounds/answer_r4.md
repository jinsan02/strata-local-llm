EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
          return VersionRange._from_specifier_set(self)

      def _check_relation_operand(self, other: object) -> None:
=======
          return VersionRange._from_specifier_set(self)

      def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          """Return the lower and upper bounds imposed by the specifiers.
          
          Returns a tuple `(lower, upper)` where each is either `None` or a tuple
          `(version, inclusive)`.
          """
          if not self._specs:
              return (None, None)
              
          if any(s.operator == "===" for s in self._specs):
              raise ValueError("Cannot compute bounds for specifier set containing ===")
              
          lower: tuple[Version, bool] | None = None
          upper: tuple[Version, bool] | None = None
          
          for spec in self._specs:
              op = spec.operator
              ver_str = spec.version
              ver = Version(ver_str.removesuffix(".*"))
              
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
                  if ver_str.endswith(".*"):
                      l = (ver, True)
                      rel = ver.release
                      next_rel = rel[:-1] + (rel[-1] + 1,)
                      u_ver = Version(f"{ver.epoch or ''}{ '.'.join(str(x) for x in next_rel) }")
                      u = (u_ver, False)
                  else:
                      l = (ver, True)
                      u = (ver, True)
              elif op == "~=":
                  l = (ver, True)
                  rel = ver.release
                  new_rel = rel[:-1]
                  u_ver = Version(f"{ver.epoch or ''}{ '.'.join(str(x) for x in new_rel[:-1] + (new_rel[-1] + 1,)) }")
                  u = (u_ver, False)
              
              if l is not None:
                  if lower is None:
                      lower = l
                  elif lower[0] == l[0]:
                      lower = lower if not lower[1] else l
                  elif lower[0] < l[0]:
                      lower = l
                      
              if u is not None:
                  if upper is None:
                      upper = u
                  elif upper[0] == u[0]:
                      upper = upper if not upper[1] else u
                  elif upper[0] > u[0]:
                      upper = u
                      
          return lower, upper

      def _check_relation_operand(self, other: object) -> None:
>>>>>>> REPLACE