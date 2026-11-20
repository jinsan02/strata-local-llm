EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  from typing import (
      Any,
      Generic,
      Literal,
      TypedDict,
      cast,
  )

  from . import licenses, requirements, specifiers, utils
=======
  from typing import (
      Any,
      Generic,
      Literal,
      TypedDict,
      cast,
  )

  from . import _parser, licenses, requirements, specifiers, utils
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
                      f"duplicate value {name!r} for {self.raw_name!r}"
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
  _process_import_namespaces = _process_import_names


  class Metadata:
=======
  _process_import_namespaces = _process_import_names


  def _extract_marker_extras(markers):
      """Extract canonical extra names from a parsed marker tree."""
      extras = set()
      for item in markers:
          if isinstance(item, tuple) and len(item) == 3:
              lhs, op, rhs = item
              if hasattr(lhs, 'value') and lhs.value == "extra" and hasattr(rhs, 'value'):
                  extras.add(rhs.value)
              elif hasattr(rhs, 'value') and rhs.value == "extra" and hasattr(lhs, 'value'):
                  extras.add(lhs.value)
          elif isinstance(item, list):
              extras.update(_extract_marker_extras(item))
      return extras


  class Metadata:
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
            provides_extra_raw = ins._raw.get("provides_extra")
            requires_dist_list = getattr(ins, "requires_dist", None)

            if isinstance(provides_extra_raw, list) and isinstance(requires_dist_list, list):
                try:
                    declared_extras = set(ins.provides_extra)
                except Exception:
                    # If provides_extra itself failed validation, skip this check
                    pass
                else:
                    for req in requires_dist_list:
                        if req.marker is not None:
                            for extra_name in _extract_marker_extras(req.marker._markers):
                                if extra_name not in declared_extras:
                                    collector.error(InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra_name!r} in requirement marker is not listed in provides-extra"
                                    ))

            collector.finalize("invalid metadata")
>>>>>>> REPLACE