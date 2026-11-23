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
                        f"duplicate extra name {normalized!r} in {self.raw_name!r}"
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

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  _process_import_namespaces = _process_import_names


  class Metadata:
=======
  _process_import_namespaces = _process_import_names


  def _get_extra_values_from_marker(marker_list: list[Any]) -> list[str]:
      result = []
      for item in marker_list:
          if isinstance(item, str):
              continue
          if isinstance(item, tuple):
              lhs, op, rhs = item
              if op.serialize() in ("==", "!="):
                  if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                      result.append(rhs.value)
                  elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                      result.append(lhs.value)
          elif isinstance(item, list):
              result.extend(_get_extra_values_from_marker(item))
      return result


  class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                    collector.error(exc)

            # Check for undeclared extras
            field_errors = {err.field for err in collector.errors}
            if "provides-extra" not in field_errors and "requires-dist" not in field_errors:
                provides_extra = getattr(ins, "provides_extra", None)
                requires_dist = getattr(ins, "requires_dist", None)
                if provides_extra is not None and requires_dist is not None:
                    declared_extras = set(provides_extra)
                    for req in requires_dist:
                        if req.marker is not None:
                            for extra_val in _get_extra_values_from_marker(req.marker._markers):
                                if extra_val not in declared_extras:
                                    collector.error(InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra_val!r} is not declared in provides-extra"
                                    ))

            collector.finalize("invalid metadata")
>>>>>>> REPLACE