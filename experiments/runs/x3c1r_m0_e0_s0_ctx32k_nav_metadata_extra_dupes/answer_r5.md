EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from __future__ import annotations

__lazy_modules__ = {
    "email.header",
    "email.parser",
    "keyword",
    "pathlib",
    f"{__spec__.parent}",
    f"{__spec__.parent}.errors",
}

import email.header
=======
from __future__ import annotations

__lazy_modules__ = {
    "email.header",
    "email.parser",
    "keyword",
    "pathlib",
    "packaging.markers",
    f"{__spec__.parent}",
    f"{__spec__.parent}.errors",
}

import email.header
>>>>>>> REPLACE

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
        for name in value:
            try:
                normalized = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            
            if normalized in seen:
                raise self._invalid_metadata(
                    "Duplicate provides-extra"
                )
            seen.add(normalized)
            normalized_names.append(normalized)
        return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
      if validate:
          collector = _ErrorCollector()
          metadata_version = None
          with collector.collect(InvalidMetadata):
              metadata_version = ins.metadata_version
              metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

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
      if validate:
          collector = _ErrorCollector()
          metadata_version = None
          with collector.collect(InvalidMetadata):
              metadata_version = ins.metadata_version
              metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

          # Make sure to check for the fields that are present, the required
          # fields (so their absence can be reported).
          fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
          # Remove fields that have already been checked.
          fields_to_check -= {"metadata_version"}

          errored_fields: set[str] = set()
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
                          errored_fields.add(key)
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
                          errored_fields.add(key)
                          continue
                  getattr(ins, key)
              except InvalidMetadata as exc:
                  collector.error(exc)
                  errored_fields.add(key)

          # Cross-field validation: undeclared extras in requires-dist markers
          if (
              "provides_extra" not in errored_fields
              and "requires_dist" not in errored_fields
          ):
              provides = ins.provides_extra
              reqs = ins.requires_dist
              if provides is not None and reqs is not None:
                  _check_undeclared_extras(provides, reqs, collector)

          collector.finalize("invalid metadata")
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
      requires: _Validator[list[str] | None] = _Validator(added="1.0")
      """:external:ref:`core-metadata-requires`"""
=======
      requires: _Validator[list[str] | None] = _Validator(added="1.0")
      """:external:ref:`core-metadata-requires`"""


def _extract_extra_comparisons(marker_list: list[Any]) -> set[str]:
    """Extract extra names compared with `extra == "value"` from a marker structure."""
    extras: set[str] = set()
    for item in marker_list:
        if isinstance(item, str):  # 'and', 'or'
            continue
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, markers.Variable) and lhs.value == "extra" and isinstance(rhs, markers.Value):
                if op.serialize() == "==":
                    extras.add(rhs.value)
            elif isinstance(rhs, markers.Variable) and rhs.value == "extra" and isinstance(lhs, markers.Value):
                if op.serialize() == "==":
                    extras.add(lhs.value)
        elif isinstance(item, list):  # Nested logical group [[...]]
            extras.update(_extract_extra_comparisons(item))
    return extras


def _check_undeclared_extras(
    provides: list[utils.NormalizedName],
    reqs: list[requirements.Requirement],
    collector: _ErrorCollector,
) -> None:
    provided_set = set(provides)
    for req in reqs:
        if req.marker is None:
            continue
        # The marker parser normalizes extra values during parsing.
        raw_extras = _extract_extra_comparisons(req.marker._markers)
        for extra_name in raw_extras:
            if extra_name not in provided_set:
                collector.error(InvalidMetadata(
                    "requires-dist",
                    f"extra {extra_name!r} is not defined in provides-extra",
                ))
>>>>>>> REPLACE