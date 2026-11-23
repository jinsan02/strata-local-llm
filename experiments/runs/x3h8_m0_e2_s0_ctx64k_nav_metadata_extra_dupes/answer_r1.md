### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from ._parser import Variable, Value
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
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
        try:
            for name in value:
                normalized_names.append(utils.canonicalize_name(name, validate=True))
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            seen = set()
            for normalized_name in normalized_names:
                if normalized_name in seen:
                    raise self._invalid_metadata(
                        f"duplicate {self.raw_name!r} value: {normalized_name!r}"
                    )
                seen.add(normalized_name)
            return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
      _process_import_namespaces = _process_import_names


class Metadata:
=======
      _process_import_namespaces = _process_import_names


def _get_extra_values(marker: Any) -> set[str]:
    """Extract normalized extra values from marker comparisons."""
    extras: set[str] = set()
    if isinstance(marker, list):
        for item in marker:
            extras.update(_get_extra_values(item))
    elif isinstance(marker, tuple) and len(marker) == 3:
        lhs, op, rhs = marker
        if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
            extras.add(rhs.value)
        elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
            extras.add(lhs.value)
    return extras


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
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
              try:
                  provides_extra = ins.provides_extra
                  requires_dist = ins.requires_dist
                  if provides_extra is not None:
                      declared_extras = set(provides_extra)
                      for req in requires_dist:
                          if req.marker is not None:
                              for extra_name in _get_extra_values(req.marker._markers):
                                  if utils.canonicalize_name(extra_name) not in declared_extras:
                                      collector.error(InvalidMetadata(
                                          "requires-dist",
                                          f"extra {extra_name!r} in marker is not "
                                          f"declared in provides-extra",
                                      ))
              except InvalidMetadata:
                  pass
>>>>>>> REPLACE