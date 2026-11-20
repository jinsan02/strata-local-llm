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
                        f"duplicate extra {normalized!r} in {self.raw_name!r}"
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
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check undeclared extras in requires_dist
            try:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
                if provides_extra is not None and requires_dist is not None:
                    provides_extra_set = set(provides_extra)
                    for req in requires_dist:
                        marker = req.marker
                        if marker is None:
                            continue
                        m = marker._markers
                        if not isinstance(m, list) or len(m) != 1:
                            continue
                        atom = m[0]
                        if not isinstance(atom, tuple) or len(atom) != 3:
                            continue
                        lhs, op, rhs = atom
                        if op.serialize() not in ("==", "!="):
                            continue
                        extra_value = None
                        if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                            extra_value = rhs.value
                        elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                            extra_value = lhs.value
                        if extra_value is not None:
                            normalized_extra = utils.canonicalize_name(extra_value)
                            if normalized_extra not in provides_extra_set:
                                collector.error(
                                    InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra_value!r} is not defined in provides_extra"
                                    )
                                )
            except InvalidMetadata:
                # Skip if provides_extra or requires_dist failed validation
                pass

            collector.finalize("invalid metadata")
>>>>>>> REPLACE