EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        try:
            for name in value:
                normalized_names.append(utils.canonicalize_name(name, validate=True))
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
=======
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        seen = set()
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"{self.raw_name!r} contains duplicate extra: {normalized!r}"
                    )
                seen.add(normalized)
                normalized_names.append(normalized)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")
=======
                  except InvalidMetadata as exc:
                      collector.error(exc)

              # Check for undeclared extras in requires_dist markers
              if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__:
                  ins._validate_extras(collector)

              collector.finalize("invalid metadata")
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
      requires: _Validator[list[str] | None] = _Validator(added="1.1")
      """``Requires`` (deprecated)"""
      provides: _Validator[list[str] | None] = _Validator(added="1.1")
      """``Provides`` (deprecated)"""
      obsoletes: _Validator[list[str] | None] = _Validator(added="1.1")
      """``Obsoletes`` (deprecated)"""

      def as_rfc822(self) -> RFC
=======
      requires: _Validator[list[str] | None] = _Validator(added="1.1")
      """``Requires`` (deprecated)"""
      provides: _Validator[list[str] | None] = _Validator(added="1.1")
      """``Provides`` (deprecated)"""
      obsoletes: _Validator[list[str] | None] = _Validator(added="1.1")
      """``Obsoletes`` (deprecated)"""

      def _validate_extras(self, collector: _ErrorCollector) -> None:
          provides_extras = self.provides_extra
          requires_dists = self.requires_dist
          if provides_extras is None:
              return
          
          provided = set(provides_extras)
          for req in requires_dists:
              if req.marker is None:
                  continue
              self._check_marker_extras(req.marker._markers, provided, collector)

      def _check_marker_extras(
          self,
          marker: list[Any],
          provided: set[utils.NormalizedName],
          collector: _ErrorCollector,
      ) -> None:
          for item in marker:
              if item in ("and", "or"):
                  continue
              if isinstance(item, list):
                  self._check_marker_extras(item, provided, collector)
              elif isinstance(item, tuple):
                  lhs, op, rhs = item
                  if op.serialize() == "==":
                      extra_val = None
                      if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                          if isinstance(rhs, markers.Value):
                              extra_val = rhs.value
                      elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                          if isinstance(lhs, markers.Value):
                              extra_val = lhs.value
                      
                      if extra_val is not None:
                          normalized_extra = utils.canonicalize_name(extra_val)
                          if normalized_extra not in provided:
                              collector.error(
                                  InvalidMetadata(
                                      "requires-dist",
                                      f"extra {normalized_extra!r} in marker is not defined in provides-extra",
                                  )
                              )

      def as_rfc822(self) -> RFC
>>>>>>> REPLACE