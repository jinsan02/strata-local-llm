### EDIT: src/packaging/metadata.py
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
          normalized_names: list[utils.NormalizedName] = []
          seen: set[utils.NormalizedName] = set()
          for name in value:
              try:
                  norm_name = utils.canonicalize_name(name, validate=True)
              except utils.InvalidName as exc:
                  raise self._invalid_metadata(
                      f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                  ) from exc

              if norm_name in seen:
                  raise self._invalid_metadata(
                      "duplicate extra name",
                  )
              seen.add(norm_name)
              normalized_names.append(norm_name)

          return normalized_names
>>>>>>> REPLACE

<<<<<<< SEARCH
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


class _Validator(Generic[T]):
=======
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


def _extract_normalized_extras(marker_ast: Any) -> set[utils.NormalizedName]:
    from .markers import Variable, Value

    extras: set[utils.NormalizedName] = set()

    if isinstance(marker_ast, str):
        return extras
    elif isinstance(marker_ast, list):
        for item in marker_ast:
            extras.update(_extract_normalized_extras(item))
    elif isinstance(marker_ast, tuple) and len(marker_ast) == 3:
        lhs, op, rhs = marker_ast
        extra_val = None
        if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
            extra_val = rhs.value
        elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
            extra_val = lhs.value

        if extra_val is not None:
            extras.add(utils.canonicalize_name(extra_val))

    return extras


class _Validator(Generic[T]):
>>>>>>> REPLACE

<<<<<<< SEARCH
              collector.finalize("invalid metadata")

          return ins
=======
              # Check for undeclared extras in requires_dist markers
              if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__:
                  _provides_extra = ins.provides_extra
                  _requires_dist = ins.requires_dist
                  for req in _requires_dist:
                      if req.marker is not None:
                          for extra_name in _extract_normalized_extras(req.marker._markers):
                              if extra_name not in _provides_extra:
                                  collector.error(
                                      InvalidMetadata(
                                          "requires-dist",
                                          f"{req.name!r} specifies {extra_name!r} as an extra, which is not provided by provides-extra",
                                      )
                                  )

              collector.finalize("invalid metadata")

          return ins
>>>>>>> REPLACE