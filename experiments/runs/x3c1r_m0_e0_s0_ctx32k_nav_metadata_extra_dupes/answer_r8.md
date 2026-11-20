### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  from . import licenses, requirements, specifiers, utils
  from . import version as version_module
  from .errors import ExceptionGroup, _ErrorCollector
=======
  from . import licenses, requirements, specifiers, utils
  from . import version as version_module
  from ._parser import Variable, Value
  from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
class _Validator(Generic[T]):
=======
def _get_extra_references(marker_list: list[Any] | None) -> list[str]:
    if marker_list is None:
        return []
    refs: list[str] = []
    for part in marker_list:
        if isinstance(part, str):
            continue
        if isinstance(part, tuple):
            lhs, op, rhs = part
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                refs.append(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                refs.append(lhs.value)
        elif isinstance(part, list):
            refs.extend(_get_extra_references(part))
    return refs


class _Validator(Generic[T]):
>>>>>>> REPLACE

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
                norm = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            if norm in seen:
                raise self._invalid_metadata(
                    f"duplicate extra {norm!r} in provides-extra"
                )
            seen.add(norm)
            normalized_names.append(norm)
        return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
          # Make sure to check for the fields that are present, the required
          # fields (so their absence can be reported).
          fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
          # Remove fields that have already been checked.
          fields_to_check -= {"metadata_version"}

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
          # Make sure to check for the fields that are present, the required
          # fields (so their absence can be reported).
          fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
          # Remove fields that have already been checked.
          fields_to_check -= {"metadata_version"}

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

          # Check for undefined extras
          provided_extras = ins.__dict__.get("provides_extra")
          required_dists = ins.__dict__.get("requires_dist")
          if provided_extras is not None and required_dists is not None:
              valid_extras = {utils.canonicalize_name(e, validate=False) for e in provided_extras}
              for req in required_dists:
                  for ref in _get_extra_references(req.marker):
                      if utils.canonicalize_name(ref, validate=False) not in valid_extras:
                          collector.error(
                              InvalidMetadata("requires-dist", f"extra {ref!r} is not provided by provides-extra")
                          )

          collector.finalize("invalid metadata")
>>>>>>> REPLACE