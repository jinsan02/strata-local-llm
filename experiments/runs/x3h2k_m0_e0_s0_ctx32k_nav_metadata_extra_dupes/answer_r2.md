### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
from packaging._parser import Variable, Value
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
        for name in value:
            try:
                canonical = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            
            if canonical in seen:
                raise self._invalid_metadata(
                    f"{canonical!r} is duplicated for {self.raw_name!r}"
                )
            seen.add(canonical)
            normalized_names.append(canonical)
        return normalized_names
>>>>>>> REPLACE

<<<<<<< SEARCH
    def _process_import_names(self, value: list[str]) -> list[str]:
=======
    def _process_import_names(self, value: list[str]) -> list[str]:


def _extract_extras_from_marker(marker) -> set[str]:
    """Extract canonicalized extra names from a marker structure."""
    extras: set[str] = set()
    if isinstance(marker, list):
        for item in marker:
            extras.update(_extract_extras_from_marker(item))
    elif isinstance(marker, tuple):
        lhs, op, rhs = marker
        if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
            extras.add(rhs.value)
        elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
            extras.add(lhs.value)
    return extras


    def _process_import_names(self, value: list[str]) -> list[str]:
>>>>>>> REPLACE

<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            if "provides_extra" not in ins._raw and "requires_dist" not in ins._raw:
                provides_extra_list = ins.provides_extra
                if provides_extra_list is not None:
                    provided_extras = set(provides_extra_list)
                    requires_dist_list = ins.requires_dist
                    if requires_dist_list is not None:
                        for req in requires_dist_list:
                            marker = req.marker
                            if marker is not None:
                                for extra_name in _extract_extras_from_marker(marker):
                                    if extra_name not in provided_extras:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra {extra_name!r} is not declared in provides-extra",
                                            )
                                        )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE