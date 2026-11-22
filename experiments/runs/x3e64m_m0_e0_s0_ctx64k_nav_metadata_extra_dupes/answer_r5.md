EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, requirements, specifiers, utils
from ._parser import Variable, Value
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


class _Validator(Generic[T]):
=======
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


def _get_extra_names_from_marker(marker_ast: list) -> set[str]:
    """Extract canonicalized extra names from `extra == "name"` comparisons in a marker AST."""
    extras: set[str] = set()

    def _extract(node: object) -> None:
        if isinstance(node, tuple):
            lhs, op, rhs = node
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(utils.canonicalize_name(lhs.value))
            if isinstance(lhs, list):
                _extract(lhs)
            if isinstance(rhs, list):
                _extract(rhs)
        elif isinstance(node, list):
            for item in node:
                _extract(item)

    _extract(marker_ast)
    return extras


class _Validator(Generic[T]):
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
                canon = utils.canonicalize_name(name, validate=True)
                if canon in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra name {canon!r} in {self.raw_name!r}"
                    )
                seen.add(canon)
                normalized_names.append(canon)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    collector.error(exc)

              collector.finalize("invalid metadata")

          return ins
=======
                    collector.error(exc)

              # Check for undeclared extras in requires_dist markers
              if (
                  "provides_extra" in ins._raw
                  and "requires_dist" in ins._raw
                  and "provides-extra" not in {e.field for e in collector.errors}
                  and "requires-dist" not in {e.field for e in collector.errors}
              ):
                  declared_extras = {utils.canonicalize_name(e) for e in ins.provides_extra}
                  for req in ins.requires_dist:
                      if req.marker is not None:
                          extra_names = _get_extra_names_from_marker(req.marker._marker)
                          for extra_name in extra_names:
                              if extra_name not in declared_extras:
                                  collector.error(
                                      InvalidMetadata(
                                          "requires-dist",
                                          f"extra {extra_name!r} in marker is not declared in provides-extra"
                                      )
                                  )

              collector.finalize("invalid metadata")

          return ins
>>>>>>> REPLACE