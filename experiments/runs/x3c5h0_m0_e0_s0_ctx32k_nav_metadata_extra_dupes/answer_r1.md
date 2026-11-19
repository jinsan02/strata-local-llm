### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


class _Validator(Generic[T]):
=======
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


def _check_undeclared_extras(
    marker_list: markers.MarkerList,
    declared_extras: set[str],
    collector: _ErrorCollector,
) -> None:
    for item in marker_list:
        if isinstance(item, tuple):
            lhs, op, rhs = item
            # Check for `extra == "..."` or `"..." == extra`
            if (isinstance(lhs, markers.Variable) and lhs.value == "extra") or \
               (isinstance(rhs, markers.Variable) and rhs.value == "extra"):
                
                val_node: Any = lhs if isinstance(lhs, markers.Value) else rhs
                
                if isinstance(val_node, markers.Value):
                    try:
                        canonical_val = utils.canonicalize_name(val_node.value, validate=True)
                        if canonical_val not in declared_extras:
                            collector.error(InvalidMetadata(
                                "requires-dist", f"Extra {canonical_val!r} is not declared"
                            ))
                    except utils.InvalidName:
                        pass # Skip invalid extra value syntax as marker parsing handles it usually.
        elif isinstance(item, list):
            _check_undeclared_extras(item, declared_extras, collector)


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
=======
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                canonical_name = utils.canonicalize_name(name, validate=True)
                if canonical_name in seen:
                    raise self._invalid_metadata(
                        f"{canonical_name!r} is duplicated for {self.raw_name!r}"
                    ) from None
                seen.add(canonical_name)
                normalized_names.append(canonical_name)
        except utils.InvalidName as exc:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            try:
                pe = ins.provides_extra
                rd = ins.requires_dist
                if pe is not None and rd is not None:
                    declared_extras = set(pe)
                    for req in rd:
                        if req.marker is not None:
                            _check_undeclared_extras(req.marker, declared_extras, collector)
            except Exception:
                pass

            collector.finalize("invalid metadata")
>>>>>>> REPLACE