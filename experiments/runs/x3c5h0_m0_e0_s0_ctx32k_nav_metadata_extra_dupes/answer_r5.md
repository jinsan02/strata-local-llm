EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from ._parser import Variable, Value
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
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
                canon_name = utils.canonicalize_name(name, validate=True)
                if canon_name in seen:
                    raise self._invalid_metadata(
                        f"{canon_name!r} is duplicated for {self.raw_name!r}"
                    )
                seen.add(canon_name)
                normalized_names.append(canon_name)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        return normalized_names
>>>>>>> REPLACE

<<<<<<< SEARCH
              collector.finalize("invalid metadata")

          return ins
=======
              # Check undeclared extras before finalizing errors.
              try:
                  provides = getattr(ins, "provides_extra")
                  requires = getattr(ins, "requires_dist")
                  if provides is not None and requires is not None:
                      self._validate_undeclared_extras(requires, provides)
              except InvalidMetadata:
                  # Validation of provides_extra or requires_dist failed; skip this check.
                  pass

              collector.finalize("invalid metadata")

          return ins
>>>>>>> REPLACE

<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names

    def _validate_undeclared_extras(
        self, requires: list[requirements.Requirement], provides: list[str]
    ) -> None:
        allowed_extras = set(provides)
        for req in requires:
            marker = req.marker
            if marker is not None:
                self._check_extra_declarations(marker, allowed_extras)

    def _check_extra_declarations(
        self, marker, allowed_extras: set[str]
    ) -> None:
        if isinstance(marker, tuple):
            lhs, op, rhs = marker
            extra_val = None
            
            # Check for `extra == value` or `value == extra`
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extra_val = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extra_val = lhs.value
            
            if extra_val is not None:
                op_str = op.serialize()
                if op_str in ("==", "!="):
                    if extra_val not in allowed_extras:
                        raise InvalidMetadata(
                            "requires-dist",
                            f"extra '{extra_val}' is not declared",
                        )
            else:
                # Recurse into logical expressions
                self._check_extra_declarations(lhs, allowed_extras)
                self._check_extra_declarations(rhs, allowed_extras)
        elif isinstance(marker, list):
            for item in marker:
                if isinstance(item, str) and item in ("and", "or"):
                    continue
                self._check_extra_declarations(item, allowed_extras)


class Metadata:
>>>>>>> REPLACE