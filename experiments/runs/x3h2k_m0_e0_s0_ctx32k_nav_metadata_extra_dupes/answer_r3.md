### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
class _Validator(Generic[T]):
=======
def _extract_extras_from_marker(marker_structure: Any) -> set[str]:
    """Extract all extra names compared to the `extra` variable in a marker structure."""
    extras: set[str] = set()
    if isinstance(marker_structure, list):
        for item in marker_structure:
            extras.update(_extract_extras_from_marker(item))
    elif isinstance(marker_structure, tuple):
        lhs, op, rhs = marker_structure
        if getattr(lhs, "value", None) == "extra" and hasattr(rhs, "value"):
            extras.add(rhs.value)
        elif getattr(rhs, "value", None) == "extra" and hasattr(lhs, "value"):
            extras.add(lhs.value)
    return extras


class _Validator(Generic[T]):
>>>>>>> REPLACE
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
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"Duplicate provides_extra value: {canonical!r}",
                    )
                seen.add(canonical)
                normalized_names.append(canonical)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
              for key in fields_to_check:
                  try:
                      if metadata_version:
                          # Can't use getattr() as that triggers descriptor protocol which
                          # will fail due to no value for the instance argument.
                          try:
                              field_metadata_version = Metadata.__dict__[key].added
                          except KeyError:
                              exc = InvalidMetadata(key, f"unrecognized field: {key!r}")
                              collector.error(exc)
                              continue
                          field_age = _VALID_METADATA_VERSIONS.index(
                              field_metadata_version
                          )
                          if field_age > metadata_age:
                              field = _RAW_TO_EMAIL_MAPPING[key]
                              exc = InvalidMetadata(
                                  field,
                                  f"{field} introduced in metadata version "
                                  f"{field_metadata_version}, not {metadata_version}",
                              )
                              collector.error(exc)
                              continue
                      getattr(ins, key)
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")
=======
              for key in fields_to_check:
                  try:
                      if metadata_version:
                          # Can't use getattr() as that triggers descriptor protocol which
                          # will fail due to no value for the instance argument.
                          try:
                              field_metadata_version = Metadata.__dict__[key].added
                          except KeyError:
                              exc = InvalidMetadata(key, f"unrecognized field: {key!r}")
                              collector.error(exc)
                              continue
                          field_age = _VALID_METADATA_VERSIONS.index(
                              field_metadata_version
                          )
                          if field_age > metadata_age:
                              field = _RAW_TO_EMAIL_MAPPING[key]
                              exc = InvalidMetadata(
                                  field,
                                  f"{field} introduced in metadata version "
                                  f"{field_metadata_version}, not {metadata_version}",
                              )
                              collector.error(exc)
                              continue
                      getattr(ins, key)
                  except InvalidMetadata as exc:
                      collector.error(exc)

              # Check for undeclared extras in requires_dist markers
              if "provides_extra" not in {e.field for e in collector.errors} and \
                 "requires_dist" not in {e.field for e in collector.errors}:
                  try:
                      provides_extra = ins.provides_extra
                      requires_dist = ins.requires_dist
                  except InvalidMetadata:
                      pass
                  else:
                      if provides_extra is not None:
                          declared_extras = set(provides_extra)
                          for req in requires_dist:
                              if req.marker is not None:
                                  marker_extras = _extract_extras_from_marker(req.marker._marker)
                                  for extra in marker_extras:
                                      if extra not in declared_extras:
                                          collector.error(
                                              InvalidMetadata(
                                                  "requires-dist",
                                                  f"Extra {extra!r} is not declared in provides-extra"
                                              )
                                          )

              collector.finalize("invalid metadata")
>>>>>>> REPLACE