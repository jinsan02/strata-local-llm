### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
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
          seen = set()
          for name in value:
              try:
                  canonicalized = utils.canonicalize_name(name, validate=True)
              except utils.InvalidName as exc:
                  raise self._invalid_metadata(
                      f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                  ) from exc
              
              if canonicalized in seen:
                  raise self._invalid_metadata(
                      f"duplicate provides-extra value: {name!r}"
                  )
              seen.add(canonicalized)
              normalized_names.append(canonicalized)
          return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _validate_extra_references(raw: RawMetadata, errors: list[Exception]) -> None:
    provides_extra = raw.get("provides_extra")
    requires_dist = raw.get("requires_dist")

    if provides_extra is None or requires_dist is None:
        return

    has_field_errors = any(
        isinstance(e, InvalidMetadata) and e.field in ("provides-extra", "requires-dist")
        for e in errors
    )
    if has_field_errors:
        return

    declared_extras = set(provides_extra)

    for req_str in requires_dist:
        try:
            marker_list = markers.parse_marker(req_str)
        except Exception:
            continue
            
        def check_marker_node(node):
            if isinstance(node, list):
                for item in node:
                    check_marker_node(item)
            elif isinstance(node, tuple):
                lhs, op, rhs = node
                op_str = op.serialize()
                if op_str in ("==", "!="):
                    extra_name = None
                    if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                        extra_name = rhs.value
                    elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                        extra_name = lhs.value
                    
                    if extra_name is not None:
                        canonicalized_extra = utils.canonicalize_name(extra_name)
                        if canonicalized_extra not in declared_extras:
                            errors.append(InvalidMetadata(
                                "requires-dist",
                                f"extra {extra_name!r} used in marker but not provided by provides-extra"
                            ))
        check_marker_node(marker_list)


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")
=======
                  except InvalidMetadata as exc:
                      collector.error(exc)

              _validate_extra_references(ins._raw, collector.errors)

              collector.finalize("invalid metadata")
>>>>>>> REPLACE