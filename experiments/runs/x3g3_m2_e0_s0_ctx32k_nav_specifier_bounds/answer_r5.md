### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
      def __contains__(self, item: UnparsedVersion) -> bool:
          """Return whether or not the item is contained in this specifier.

          :param item: The item to check for.

          This is used for the ``in`` operator and behaves the same as
          :meth:`contains` with no ``prereleases`` argument passed.

          >>> "1.2.3" in SpecifierSet(">=1.0.0,!=1.0.1")
          True
          >>> Version("1.2.3") in SpecifierSet(">=1.0.0,!=1.0.1")
          True
          >>> "1.0.1" in SpecifierSet(">=1.0.0,!=1.0.1")
          False
          >>> "1.3.0a1" in SpecifierSet(">=1.0.0,!=1.0.1")
          True
          >>> "1.3.0a1" in SpecifierSet(">=1.0.0,!=1.0.1", prereleases=True)
          True
          """
          return self.contains(item)
=======
      def bounds(
          self,
      ) -> tuple[
          tuple[Version, bool] | None,
          tuple[Version, bool] | None,
      ]:
          """Return the ``(lower, upper)`` bounds of the specifier set.

          Each bound is either ``None`` (no limit) or a tuple of
          ``(Version, inclusive)`` where ``inclusive`` is ``True`` if the
          version is included in the bound.

          - ``lower`` is the maximum of all lower bounds.
          - ``upper`` is the minimum of all upper bounds.
          - If bounds share the same version, the non-inclusive one wins.
          - ``===`` specifiers raise :exc:`ValueError`.
          - Empty specifier sets return ``(None, None)``.

          >>> SpecifierSet(">=1.0, <2.0").bounds()
          ((<Version('1.0')>, True), (<Version('2.0')>, False))
          >>> SpecifierSet("==1.2.*").bounds()
          ((<Version('1.2')>, True), (<Version('1.3')>, False))
          >>> SpecifierSet("~=1.4.5").bounds()
          ((<Version('1.4.5')>, True), (<Version('1.5')>, False))
          >>> SpecifierSet("").bounds()
          (None, None)
          >>> SpecifierSet("===1.0").bounds()
          Traceback (most recent call last):
              ...
          ValueError: === operator is not supported for bounds
          """
          if not self._specs:
              return (None, None)

          if any(s.operator == "===" for s in self._specs):
              raise ValueError("=== operator is not supported for bounds")

          lower: tuple[Version, bool] | None = None
          upper: tuple[Version, bool] | None = None

          for spec in self._specs:
              l, u = _specifier_bounds(spec)

              if l is not None:
                  if lower is None or l > lower:
                      lower = l
              if u is not None:
                  if upper is None or u < upper:
                      upper = u

          return (lower, upper)

      def __contains__(self, item: UnparsedVersion) -> bool:
          """Return whether or not the item is contained in this specifier.

          :param item: The item to check for.

          This is used for the ``in`` operator and behaves the same as
          :meth:`contains` with no ``prereleases`` argument passed.

          >>> "1.2.3" in SpecifierSet(">=1.0.0,!=1.0.1")
          True
          >>> Version("1.2.3") in SpecifierSet(">=1.0.0,!=1.0.1")
          True
          >>> "1.0.1" in SpecifierSet(">=1.0.0,!=1.0.1")
          False
          >>> "1.3.0a1" in SpecifierSet(">=1.0.0,!=1.0.1")
          True
          >>> "1.3.0a1" in SpecifierSet(">=1.0.0,!=1.0.1", prereleases=True)
          True
          """
          return self.contains(item)
>>>>>>> REPLACE
<<<<<<< SEARCH
  def _apply_prereleases_filter(
      matches: Iterable[Any],
      key: Callable[[Any], UnparsedVersion] | None,
      prereleases: bool | None,
  ) -> Iterator[Any]:
=======
  def _next_release(version: Version) -> Version:
      """Compute the next release version after *version*."""
      release = list(version.release)
      release[-1] += 1
      parts = [str(x) for x in release]
      if version.epoch:
          return Version(f"{version.epoch}!{'.'.join(parts)}")
      return Version(".".join(parts))


  def _next_compat_release(version: Version) -> Version:
      """Compute the upper bound release for a ``~=`` specifier."""
      release = list(version.release)
      # PEP 440 requires at least two digits for ~=
      if len(release) < 2:
          release[-1] += 1
      else:
          release = release[:-2] + [release[-2] + 1]
      parts = [str(x) for x in release]
      if version.epoch:
          return Version(f"{version.epoch}!{'.'.join(parts)}")
      return Version(".".join(parts))


  def _specifier_bounds(
      spec: Specifier,
  ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
      """Return the ``(lower, upper)`` bounds for a single specifier.

      Each bound is ``None`` or a tuple ``(Version, inclusive)``.
      Internal comparison uses ``(version, inclusive)`` for lower bounds
      (max wins) and ``(version, not inclusive)`` for upper bounds (min wins).
      """
      op = spec.operator
      ver_str = spec.version

      if op == "===":
          raise ValueError("=== operator is not supported for bounds")

      v = spec._require_spec_version()

      if op == ">=":
          return ((v, True), None)
      if op == ">":
          return ((v, False), None)
      if op == "<=":
          return (None, (v, False))
      if op == "<":
          return (None, (v, True))
      if op == "==":
          if ver_str.endswith(".*"):
              lower = (v, True)
              upper = (_next_release(v), True)
              return (lower, upper)
          else:
              return ((v, True), (v, False))
      if op == "~=":
          lower = (v, True)
          upper = (_next_compat_release(v), True)
          return (lower, upper)
      if op == "!=":
          return (None, None)

      return (None, None)


  def _apply_prereleases_filter(
      matches: Iterable[Any],
      key: Callable[[Any], UnparsedVersion] | None,
      prereleases: bool | None,
  ) -> Iterator[Any]:
>>>>>>> REPLACE