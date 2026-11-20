EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from .errors import ExceptionGroup, _ErrorCollector
=======
from .errors import ExceptionGroup, _ErrorCollector
from ._parser import Variable, Value, Op
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
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"Duplicate provides-extra: {canonical!r}"
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

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  collector.finalize("invalid metadata")

        return ins
=======
  collector.finalize("invalid metadata")

        return ins

    @staticmethod
    def _validate_extra_in_marker(
        marker: list,
        provides_extra: set[str],
        collector: _ErrorCollector,
        req_str: str,
    ) -> None:
        for item in marker:
            if isinstance(item, str):
                continue
            if isinstance(item, list):
                Metadata._validate_extra_in_marker(
                    item, provides_extra, collector, req_str
                )
            elif isinstance(item, tuple):
                lhs, op, rhs = item
                if op.serialize() in ("==", "!="):
                    extra_value = None
                    if (
                        isinstance(lhs, Variable)
                        and lhs.value == "extra"
                        and isinstance(rhs, Value)
                    ):
                        extra_value = rhs.value
                    elif (
                        isinstance(rhs, Variable)
                        and rhs.value == "extra"
                        and isinstance(lhs, Value)
                    ):
                        extra_value = lhs.value

                    if extra_value is not None:
                        try:
                            canonical_extra = utils.canonicalize_name(extra_value)
                        except utils.InvalidName:
                            continue
                        if canonical_extra not in provides_extra:
                            collector.error(InvalidMetadata(
                                "requires-dist",
                                f"extra {extra_value!r} in requirement {req_str!r} "
                                f"is not defined in provides-extra",
                            ))
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

                collector.finalize("invalid metadata")
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check undeclared extras in requires_dist markers
            if "provides-extra" not in {e.field for e in collector.errors}:
                try:
                    pe = ins.provides_extra
                    if pe is not None:
                        pe_set = set(pe)
                        if "requires-dist" not in {e.field for e in collector.errors}:
                            for req in ins.requires_dist:
                                if req.marker is not None:
                                    Metadata._validate_extra_in_marker(
                                        req.marker._marker,
                                        pe_set,
                                        collector,
                                        req.marker.marker,
                                    )
                except InvalidMetadata:
                    pass

                collector.finalize("invalid metadata")
>>>>>>> REPLACE