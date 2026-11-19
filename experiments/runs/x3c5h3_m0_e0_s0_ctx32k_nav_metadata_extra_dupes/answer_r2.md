### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  import typing
  from typing import (
      Any,
      Generic,
      Literal,
      TypedDict,
      cast,
  )

  from . import licenses, requirements, specifiers, utils
=======
  import typing
  from typing import (
      Any,
      Generic,
      Literal,
      TypedDict,
      cast,
  )

  from . import _parser
  from . import licenses, requirements, specifiers, utils
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
                canonical_name = utils.canonicalize_name(name, validate=True)
                if canonical_name in seen:
                    raise self._invalid_metadata(f"duplicate extra name {canonical_name!r}")
                seen.add(canonical_name)
                normalized_names.append(canonical_name)
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


def _check_extras_in_markers(markers, provides_extra_set):
    """Check if extra names in markers are defined in `provides_extra`."""
    errors = []

    def visit(marker):
        if isinstance(marker, list):
            for item in marker:
                visit(item)
        elif isinstance(marker, tuple):
            # MarkerAtom: (lhs, op, rhs)
            lhs, op, rhs = marker
            
            # Check for extra == "value" or "value" == extra
            if isinstance(lhs, _parser.Variable) and lhs.value == "extra":
                if isinstance(rhs, _parser.Value):
                    extra_name = rhs.value
                    if extra_name not in provides_extra_set:
                        errors.append(InvalidMetadata("requires-dist", f"required extra '{extra_name}' is not defined"))
            elif isinstance(rhs, _parser.Variable) and rhs.value == "extra":
                if isinstance(lhs, _parser.Value):
                    extra_name = lhs.value
                    if extra_name not in provides_extra_set:
                        errors.append(InvalidMetadata("requires-dist", f"required extra '{extra_name}' is not defined"))

    visit(markers)
    return errors


class Metadata:
>>>>>>> REPLACE
<<<<<<< SEARCH
            # Remove fields that have already been checked.
            fields_to_check -= {"metadata_version"}

            for key in fields_to_check:
=======
            # Remove fields that have already been checked.
            fields_to_check -= {"metadata_version", "provides_extra", "requires_dist"}

            # Validate provides_extra (checks for duplicates) and requires_dist (checks extra declarations)
            raw_provides_extra = data.get("provides_extra")
            validated_provides_extra = None
            if raw_provides_extra is not None:
                try:
                    validated_provides_extra = Metadata.__dict__["provides_extra"]._process_provides_extra(raw_provides_extra)
                    ins.__dict__["provides_extra"] = validated_provides_extra
                except InvalidMetadata as exc:
                    collector.error(exc)

            raw_requires_dist = data.get("requires_dist")
            if raw_requires_dist is not None and validated_provides_extra is not None:
                try:
                    provides_extra_set = set(validated_provides_extra)
                    for req_str in raw_requires_dist:
                        # Check extra declarations in markers
                        req = requirements.Requirement(req_str)
                        if req.marker is not None:
                            marker_errors = _check_extras_in_markers(
                                req.marker._markers, provides_extra_set
                            )
                            for err in marker_errors:
                                collector.error(err)
                except requirements.InvalidRequirement as exc:
                    collector.error(InvalidMetadata("requires-dist", f"{req_str!r} is invalid for requires-dist", cause=exc))

            for key in fields_to_check:
>>>>>>> REPLACE