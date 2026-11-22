### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
from ._parser import Variable, Value
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
        normalized_names = []
        seen_names = set()
        for name in value:
            try:
                normalized = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            
            if normalized in seen_names:
                raise self._invalid_metadata(
                    f"{normalized!r} is a duplicate provides-extra"
                )
            seen_names.add(normalized)
            normalized_names.append(normalized)
        return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
              fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
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
              fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
              fields_to_check -= {"metadata_version"}

              valid_fields = set()
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
                      valid_fields.add(key)
                  except InvalidMetadata as exc:
                      collector.error(exc)

              if "provides_extra" in valid_fields and "requires_dist" in valid_fields:
                  provides_extras = set(ins.provides_extra)
                  for req in ins.requires_dist:
                      if req.marker is not None:
                          for extra in _find_extra_values(req.marker._markers):
                              if utils.canonicalize_name(extra) not in provides_extras:
                                  collector.error(
                                      InvalidMetadata(
                                          "requires-dist",
                                          f"extra {extra!r} in requirement {req.name!r} is not declared in provides_extra"
                                      )
                                  )

              collector.finalize("invalid metadata")
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  from .licenses import NormalizedLicenseExpression
  from .version import Version
=======
  from .licenses import NormalizedLicenseExpression
  from .version import Version


  def _find_extra_values(marker_list: list) -> list[str]:
      """Extract literal extra values from `extra == "value"` comparisons in a marker tree."""
      extras = []
      for item in marker_list:
          if isinstance(item, tuple):
              lhs, op, rhs = item
              if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                  if op.value == "==":
                      extras.append(rhs.value)
              elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                  if op.value == "==":
                      extras.append(lhs.value)
          elif isinstance(item, list):
              extras.extend(_find_extra_values(item))
      return extras
>>>>>>> REPLACE