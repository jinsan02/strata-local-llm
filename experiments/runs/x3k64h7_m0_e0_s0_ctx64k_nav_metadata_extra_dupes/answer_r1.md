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
  _LIST_FIELDS = {
=======
  def _extract_extra_names(marker: list[object]) -> list[str]:
      """Extract extra names from a marker list."""
      names: list[str] = []
      for item in marker:
          if item in ("and", "or"):
              continue
          if isinstance(item, tuple):
              lhs, op, rhs = item
              if op.serialize() == "==":
                  if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                      names.append(rhs.value)
                  elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                      names.append(lhs.value)
          elif isinstance(item, list):
              names.extend(_extract_extra_names(item))
      return names

  _LIST_FIELDS = {
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            failed_fields = {e.field for e in collector.errors}
            if "provides-extra" not in failed_fields and "requires-dist" not in failed_fields:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
                if provides_extra is not None and requires_dist is not None:
                    for req in requires_dist:
                        if req.marker is not None:
                            for extra_name in _extract_extra_names(req.marker._markers):
                                if utils.canonicalize_name(extra_name) not in provides_extra:
                                    collector.error(InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra_name!r} is not declared in provides-extra"
                                    ))

            collector.finalize("invalid metadata")
>>>>>>> REPLACE