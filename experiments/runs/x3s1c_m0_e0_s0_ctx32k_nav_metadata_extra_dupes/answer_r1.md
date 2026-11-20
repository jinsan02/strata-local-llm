EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from ._parser import Variable, Value, Op
from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
_RAW_TO_EMAIL_MAPPING = {raw: email for email, raw in _EMAIL_TO_RAW_MAPPING.items()}


# A bare "\r" makes the email generator raise ``HeaderWriteError``, and on
=======
_RAW_TO_EMAIL_MAPPING = {raw: email for email, raw in _EMAIL_TO_RAW_MAPPING.items()}


def _find_extra_comparisons(marker: Any) -> list[str]:
    """Extract extra comparison values from a marker structure."""
    if isinstance(marker, tuple):
        lhs, op, rhs = marker
        if op.serialize() in ("==", "!="):
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    return [rhs.value]
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    return [lhs.value]
    elif isinstance(marker, list):
        result: list[str] = []
        for item in marker:
            result.extend(_find_extra_comparisons(item))
        return result
    return []


# A bare "\r" makes the email generator raise ``HeaderWriteError``, and on
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
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"{self.raw_name!r} contains duplicate extra: {normalized!r}"
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

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    @classmethod
    def from_email(cls, data: bytes | str, *, validate: bool = True) -> Metadata:
=======
    def _check_undeclared_extras(self) -> None:
        if self.provides_extra is None or self.requires_dist is None:
            return
        declared = set(self.provides_extra)
        for req in self.requires_dist:
            if req.marker is not None:
                extra_vals = _find_extra_comparisons(req.marker._markers)
                for val in extra_vals:
                    if val not in declared:
                        raise InvalidMetadata(
                            "requires-dist",
                            f"extra {val!r} not declared in provides-extra",
                        )

    @classmethod
    def from_email(cls, data: bytes | str, *, validate: bool = True) -> Metadata:
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check undeclared extras after all fields are validated
            if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__:
                try:
                    ins._check_undeclared_extras()
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE