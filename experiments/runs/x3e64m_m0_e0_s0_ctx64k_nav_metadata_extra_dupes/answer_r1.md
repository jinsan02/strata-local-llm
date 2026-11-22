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
  from .markers import InvalidMarker, Marker
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
                canon = utils.canonicalize_name(name, validate=True)
                if canon in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra name {name!r}",
                    )
                seen.add(canon)
                normalized_names.append(canon)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

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

              # Validate provides_extra and requires_dist first to get their values
              provides_extra_val = None
              requires_dist_val = None
              try:
                  provides_extra_val = getattr(ins, "provides_extra")
              except InvalidMetadata:
                  pass
              try:
                  requires_dist_val = getattr(ins, "requires_dist")
              except InvalidMetadata:
                  pass

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
              if provides_extra_val is not None and requires_dist_val is not None:
                  for req in requires_dist_val:
                      if req.marker:
                          try:
                              m = Marker(req.marker)
                              for atom in m._markers:
                                  if isinstance(atom, tuple):
                                      lhs, op, rhs = atom
                                      if isinstance(lhs, Variable) and lhs.value == "extra":
                                          if isinstance(rhs, Value) and rhs.value not in provides_extra_val:
                                              collector.error(
                                                  InvalidMetadata(
                                                      "requires-dist",
                                                      f"{rhs.value!r} is not declared in provides_extra",
                                                  )
                                              )
                                      elif isinstance(rhs, Variable) and rhs.value == "extra":
                                          if isinstance(lhs, Value) and lhs.value not in provides_extra_val:
                                              collector.error(
                                                  InvalidMetadata(
                                                      "requires-dist",
                                                      f"{lhs.value!r} is not declared in provides_extra",
                                                  )
                                              )
                          except InvalidMarker:
                              pass

              collector.finalize("invalid metadata")
>>>>>>> REPLACE