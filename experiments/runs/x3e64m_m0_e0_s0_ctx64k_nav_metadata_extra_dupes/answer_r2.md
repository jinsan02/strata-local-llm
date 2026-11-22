### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from .errors import ExceptionGroup, _ErrorCollector
=======
from .errors import ExceptionGroup, _ErrorCollector
from ._parser import Variable, Value
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
                        f"{name!r} is a duplicate extra"
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


def _check_undeclared_extras(
    requires_dist: list[requirements.Requirement],
    provides_extra: list[utils.NormalizedName],
    collector: _ErrorCollector,
) -> None:
    declared = set(provides_extra)
    for req in requires_dist:
        if req.marker is None:
            continue
        _find_undeclared_extras(req.marker._markers, declared, collector)


def _find_undeclared_extras(
    marker_list: list[Any],
    declared_extras: set[str],
    collector: _ErrorCollector,
) -> None:
    for item in marker_list:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            _find_undeclared_extras(item, declared_extras, collector)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            extra_val = None
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extra_val = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extra_val = lhs.value
            
            if extra_val is not None:
                canonical_extra = utils.canonicalize_name(extra_val)
                if canonical_extra not in declared_extras:
                    collector.error(
                        InvalidMetadata(
                            "requires-dist",
                            f"extra {extra_val!r} is not declared in provides-extra"
                        )
                    )


class Metadata:
>>>>>>> REPLACE

<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            if (
                "provides_extra" in ins.__dict__
                and "requires_dist" in ins.__dict__
                and ins.provides_extra is not None
                and ins.requires_dist is not None
            ):
                _check_undeclared_extras(ins.requires_dist, ins.provides_extra, collector)

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE