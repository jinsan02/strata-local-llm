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
def _extract_extra_names(marker_list: list) -> set[str]:
    extras = set()
    for item in marker_list:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.update(_extract_extra_names(item))
        elif isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            if str(op) in ("==", "!="):
                if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                    extras.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                    extras.add(lhs.value)
    return extras


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
            for norm_name in normalized_names:
                if norm_name in seen:
                    raise self._invalid_metadata(
                        f"duplicate provides-extra: {norm_name!r}"
                    )
                seen.add(norm_name)
            return normalized_names
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
              provides_extra_val = ins.__dict__.get("provides_extra")
              requires_dist_val = ins.__dict__.get("requires_dist")
              if provides_extra_val is not None and requires_dist_val is not None:
                  canonical_provides = set(provides_extra_val)
                  for req in requires_dist_val:
                      if req.marker is not None:
                          for extra_name in _extract_extra_names(req.marker._markers):
                              if utils.canonicalize_name(extra_name)

I have thought about this long enough; time to give my answer.
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
def _extract_extra_names(marker_list: list) -> set[str]:
    extras = set()
    for item in marker_list:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.update(_extract_extra_names(item))
        elif isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            if str(op) in ("==", "!="):
                if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                    extras.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                    extras.add(lhs.value)
    return extras


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
            for norm_name in normalized_names:
                if norm_name in seen:
                    raise self._invalid_metadata(
                        f"duplicate provides-extra: {norm_name!r}"
                    )
                seen.add(norm_name)
            return normalized_names
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