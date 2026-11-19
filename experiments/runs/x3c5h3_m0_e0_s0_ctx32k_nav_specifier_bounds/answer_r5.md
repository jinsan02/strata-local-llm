EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
          return _apply_prereleases_filter(iterable, key, prereleases)


def _pep440_filter_prereleases(
=======
          return _apply_prereleases_filter(iterable, key, prereleases)

      def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          """Return the calculated lower and upper bounds of the SpecifierSet.
          
          Returns a tuple (lower, upper), where each is either ``None`` or a
          ``(Version, inclusive: bool)`` tuple.
          """
          if self._has_arbitrary:
              raise ValueError("Cannot determine bounds for '===' specifier")
          
          lower: tuple[Version, bool] | None = None
          upper: tuple[Version, bool] | None = None
          
          for spec in self._specs:
              op = spec._spec[0]
              ver_str = spec._spec[1]
              
              # Use the already parsed version if available (e.g., base for wildcards)
              parsed_v = spec._spec_version if spec._spec_version is not None else Version(ver_str)
              
              lower_candidate: tuple[Version, bool] | None = None
              upper_candidate: tuple[Version, bool] | None = None
              
              if op == ">=":
                  lower_candidate = (parsed_v, True)
              elif op == ">":
                  lower_candidate = (parsed_v, False)
              elif op == "<=":
                  upper_candidate = (parsed_v, True)
              elif op == "<":
                  upper_candidate = (parsed_v, False)
              elif op == "==":
                  if ver_str.endswith(".*"):
                      lower_candidate = (parsed_v, True)
                      # next release: trim trailing zeros, increment last digit
                      r = list(parsed_v.release)
                      while len(r) > 1 and r[-1] == 0:
                          r.pop()
                      if not r:
                          new_rel = (0,)
                      else:
                          r[-1] += 1
                          new_rel = tuple(r)
                      upper_candidate = (Version(epoch=parsed_v.epoch, release=new_rel), False)
                  else:
                      lower_candidate = (parsed_v, True)
                      upper_candidate = (parsed_v, True)
              elif op == "~=":
                  lower_candidate = (parsed_v, True)
                  # ~= base version: trim trailing zeros, increment last digit
                  r = list(parsed_v.release)
                  while len(r) > 1 and r[-1] == 0:
                      r.pop()
                  if not r:
                      new_rel = (1,)
                  else:
                      r[-1] += 1
                      new_rel = tuple(r)
                  upper_candidate = (Version(epoch=parsed_v.epoch, release=new_rel), False)
              elif op == "!=":
                  pass # != does not constrain bounds directly
              else:
                  raise ValueError(f"Unsupported operator {op}")
                  
              if lower_candidate is not None:
                  if lower is None or \
                     lower_candidate[0] > lower[0] or \
                     (lower_candidate[0] == lower[0] and not lower_candidate[1]):
                      lower = lower_candidate
                      
              if upper_candidate is not None:
                  if upper is None or \
                     upper_candidate[0] < upper[0] or \
                     (upper_candidate[0] == upper[0] and not upper_candidate[1]):
                      upper = upper_candidate
                      
          return (lower, upper)


def _pep440_filter_prereleases(
>>>>>>> REPLACE