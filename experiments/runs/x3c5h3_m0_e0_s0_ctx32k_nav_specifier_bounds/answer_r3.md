EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
      def is_unsatisfiable(self) -> bool:
=======
      def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          """Return the combined `(lower, upper)` bounds of all specifiers.
          
        :raises ValueError: If a ``===`` specifier is present.
        """
          if self._has_arbitrary:
              raise ValueError("SpecifierSet cannot contain '===' for bounds()")
          
          lower: tuple[Version, bool] | None = None
          upper: tuple[Version, bool] | None = None
          
          for spec in self._specs:
              op = spec.operator
              ver_str = spec.version
              
              low_con: tuple[Version, bool] | None = None
              up_con: tuple[Version, bool] | None = None
              
              if op == "==":
                  if ver_str.endswith(".*"):
                      v_base = Version(ver_str[:-2])
                      low_con = (v_base, True)
                      rel = v_base.release
                      if len(rel) > 1:
                          new_rel = list(rel[:-1])
                          new_rel[-1] += 1
                          up_str = ".".join(map(str, new_rel))
                      else:
                          up_str = str(rel[-1] + 1)
                      
                      if v_base.epoch:
                          up_con = (Version(f"{v_base.epoch}!{up_str}"), False)
                      else:
                          up_con = (Version(up_str), False)
                  else:
                      v = spec._require_spec_version()
                      low_con = (v, True)
                      up_con = (v, True)
              elif op == "~=":
                  v = spec._require_spec_version()
                  low_con = (v, True)
                  rel = v.release
                  if len(rel) >= 2:
                      new_rel = list(rel[:-1])
                      new_rel[-1] += 1
                      up_str = ".".join(map(str, new_rel))
                      if v.epoch:
                          up_con = (Version(f"{v.epoch}!{up_str}"), False)
                      else:
                          up_con = (Version(up_str), False)
              elif op == ">=":
                  v = spec._require_spec_version()
                  low_con = (v, True)
              elif op == ">":
                  v = spec._require_spec_version()
                  low_con = (v, False)
              elif op == "<=":
                  v = spec._require_spec_version()
                  up_con = (v, True)
              elif op == "<":
                  v = spec._require_spec_version()
                  up_con = (v, False)
              
              # Merge lower bound
              if low_con is not None:
                  if lower is None:
                      lower = low_con
                  else:
                      cv, ci = lower
                      nv, ni = low_con
                      if nv > cv:
                          lower = low_con
                      elif nv == cv and not ni: # exclusive wins over inclusive
                          lower = low_con
              
              # Merge upper bound
              if up_con is not None:
                  if upper is None:
                      upper = up_con
                  else:
                      cv, ci = upper
                      nv, ni = up_con
                      if nv < cv:
                          upper = up_con
                      elif nv == cv and not ni: # exclusive wins over inclusive
                          upper = up_con
                          
          return (lower, upper)

      def is_unsatisfiable(self) -> bool:
>>>>>>> REPLACE