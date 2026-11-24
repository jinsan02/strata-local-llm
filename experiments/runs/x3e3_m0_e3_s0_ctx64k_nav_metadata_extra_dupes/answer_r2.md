### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  from . import licenses, requirements, specifiers, utils
  from . import version as version_module
  from .errors import ExceptionGroup, _ErrorCollector
=======
  from . import licenses, requirements, specifiers, utils
  from . import version as version_module
  from . _parser import Variable, Value, Op
  from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  _process_import_namespaces = _process_import_names


  class Metadata:
=======
  _process_import_namespaces = _process_import_names


  def _extract_extra_values(marker, extras_found):
      """Extract canonicalized extra names compared with the `extra` variable."""
      if isinstance(marker, tuple):
          lhs, op, rhs = marker
          if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
              if op.serialize() in ("==", "!="):
                  extras_found.append(rhs.value)
          elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
              if op.serialize() in ("==", "!="):
                  extras_found.append(lhs.value)
      elif isinstance(marker, list):
          for item in marker:
              _extract_extra_values(item, extras_found)


  class Metadata:
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
              for n in normalized_names:
                  if n in seen:
                      raise self._invalid_metadata(
                          f"duplicate extra name {n!r}",
                      )
                  seen.add(n)
              return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")

          return ins
=======
                  except InvalidMetadata as exc:
                      collector.error(exc)

              # Check for undeclared extras in requires_dist markers
              if "provides_extra" in fields_to_check and "requires_dist" in fields_to_check:
                  failed_fields = {
                      e.field for e in collector.errors if isinstance(e, InvalidMetadata)
                  }
                  if (
                      "provides-extra" not in failed_fields
                      and "requires-dist" not in failed_fields
                  ):
                      provides_extras = ins.provides_extra
                      requires_dists = ins.requires_dist
                      if provides_extras is not None and requires_dists is not None:
                          declared = set(provides_extras)
                          for req in requires_dists:
                              if req.marker is not None:
                                  extras_found = []
                                  _extract_extra_values(req.marker, extras_found)
                                  for extra in extras_found:
                                      if extra not in declared:
                                          collector.error(
                                              InvalidMetadata(
                                                  "requires-dist",
                                                  f"extra {extra!r} in marker is not declared in provides-extra",
                                              )
                                          )

              collector.finalize("invalid metadata")

          return ins
>>>>>>> REPLACE