### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
   from . import licenses, requirements, specifiers, utils
   from . import version as version_module
   from .errors import ExceptionGroup, _ErrorCollector
=======
   from . import licenses, markers, requirements, specifiers, utils
   from . import version as version_module
   from ._parser import Variable, Value
   from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  _process_import_namespaces = _process_import_names


  class Metadata:
=======
  _process_import_namespaces = _process_import_names


  def _validate_undeclared_extras(
      requires_dist: list[requirements.Requirement],
      provides_extra: list[utils.NormalizedName],
      collector: _ErrorCollector,
  ) -> None:
      declared = set(provides_extra)
      for req in requires_dist:
          _check_extra_in_marker(req.marker._markers, declared, collector)


  def _check_extra_in_marker(
      marker: list | tuple,
      declared: set[utils.NormalizedName],
      collector: _ErrorCollector,
  ) -> None:
      if isinstance(marker, list):
          for m in marker:
              _check_extra_in_marker(m, declared, collector)
      elif isinstance(marker, tuple):
          lhs, op, rhs = marker
          if op.serialize() == "==":
              if isinstance(lhs, Variable) and lhs.value == "extra":
                  if isinstance(rhs, Value):
                      if rhs.value not in declared:
                          collector.error(
                              InvalidMetadata(
                                  "requires-dist",
                                  f"{rhs.value!r} is not declared in provides-extra",
                              )
                          )
              elif isinstance(rhs, Variable) and rhs.value == "extra":
                  if isinstance(lhs, Value):
                      if lhs.value not in declared:
                          collector.error(
                              InvalidMetadata(
                                  "requires-dist",
                                  f"{lhs.value!r} is not declared in provides-extra",
                              )
                          )


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
              if len(normalized_names) != len(set(normalized_names)):
                  raise self._invalid_metadata(
                      f"duplicate values in {self.raw_name!r}"
                  )
              return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
           collector.finalize("invalid metadata")

       return ins
=======
           # Check for undeclared extras in requires_dist
           failed_fields = {exc.field for exc in collector.errors}
           if "provides-extra" not in failed_fields and "requires-dist" not in failed_fields:
               provides_extra = getattr(ins, "provides_extra", None)
               requires_dist = getattr(ins, "requires_dist", None)
               if provides_extra is not None and requires_dist is not None:
                   _validate_undeclared_extras(requires_dist, provides_extra, collector)

           collector.finalize("invalid metadata")

       return ins
>>>>>>> REPLACE