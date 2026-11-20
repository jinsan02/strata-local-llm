EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
      def is_disjoint(self, other: SpecifierSet) -> bool:
          """Return whether this set and other share no matching versions.
=======
      def bounds(
          self,
      ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
          """Return the lower and upper bounds imposed by this SpecifierSet.

          Returns a tuple ``(lower, upper)`` where each is either ``None`` 
          (unbounded) or a ``(version, inclusive)`` tuple. 
          Raises ``ValueError`` if any specifier uses the ``===`` operator.
          Prerelease settings are ignored for bound computation.
          """
          if self._has_arbitrary:
              raise ValueError("cannot compute bounds for sets containing === specifiers")

          lower: tuple[Version, bool] | None = None
          upper: tuple[Version, bool] | None = None

          def _make_ver(epoch: int, release: tuple[int, ...]) -> Version:
              s = f"{epoch}" if epoch else ""
              return Version(f"{s}{'.' + '.'.join(map(str, release)) if release else ''}")

          for spec in self._specs:
              op, ver_str = spec._spec
              v = Version(ver_str)
              
              # Strip non-release components (pre, post, dev, local) for consistent comparison
              trimmed_v = _make_ver(v.epoch, v.release)
              
              lo: tuple[Version, bool] | None = None
              hi: tuple[Version, bool] | None = None
              
              if op == ">=":
                  lo = (trimmed_v, True)
              elif op == ">":
                  lo = (trimmed_v, False)
              elif op == "<=":
                  hi = (trimmed_v, True)
              elif op == "<":
                  hi = (trimmed_v, False)
              elif op == "==":
                  if ver_str.endswith(".*"):
                      lo = (trimmed_v, True)
                      rel = trimmed_v.release
                      up_rel = rel[:-1] + (rel[-1] + 1,)
                      hi = (_make_ver(v.epoch, up_rel), False)
                  else:
                      lo = (trimmed_v, True)
                      hi = (trimmed_v, True)
              elif op == "~=":
                  lo = (trimmed_v, True)
                  rel = trimmed_v.release
                  if len(rel) == 1:
                      up_rel = (rel[0] + 1,)
                  else:
                      up_rel = rel[:-2] + (rel[-2] + 1,)
                  hi = (_make_ver(v.epoch, up_rel), False)
              
              if lo is not None:
                  if lower is None or trimmed_v > lower[0]:
                      lower = lo
                  elif trimmed_v == lower[0]:
                      lower = (trimmed_v, False)
                      
              if hi is not None:
                  if upper is None or trimmed_v > upper[0]:
                      upper = hi
                  elif trimmed_v == upper[0]:
                      upper = (trimmed_v, False)
                      
          return lower, upper

      def is_disjoint(self, other: SpecifierSet) -> bool:
          """Return whether this set and other share no matching versions.
>>>>>>> REPLACE