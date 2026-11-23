### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
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
        normalized_names: list[utils.NormalizedName] = []
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"{name!r} is a duplicate extra for {self.raw_name!r}"
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

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _check_undeclared_extras(
    requires_dist: list[requirements.Requirement],
    provides_extra: list[utils.NormalizedName],
) -> list[InvalidMetadata]:
    errors: list[InvalidMetadata] = []
    declared_set = set(provides_extra)
    
    for req in requires_dist:
        if req.marker is not None:
            # Traverse the marker tree
            stack = [req.marker._markers]
            while stack:
                node = stack.pop()
                if isinstance(node, str):  # "and" or "or"
                    continue
                if isinstance(node, tuple):  # MarkerItem
                    lhs, op, rhs = node
                    if op.serialize() == "==":
                        if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                            extra_name = utils.canonicalize_name(rhs.value)
                            if extra_name not in declared_set:
                                errors.append(
                                    InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra_name!r} in requirement "
                                        f"{req.name!r} is not in Provides-Extra",
                                    )
                                )
                        elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                            extra_name = utils.canonicalize_name(lhs.value)
                            if extra_name not in declared_set:
                                errors.append(
                                    InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra_name!r} in requirement "
                                        f"{req.name!r} is not in Provides-Extra",
                                    )
                                )
                else:
                    # It's a list (MarkerList)
                    stack.extend(node)
                    
    return errors


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
            # Make sure to check for the fields that are present, the required
            # fields (so their absence can be reported).
            fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
            # Remove fields that have already been checked.
            fields_to_check -= {"metadata_version"}

            for key in fields_to_check:
                try:
                    if metadata_version:
                        # Can't use getattr() as that triggers descriptor protocol which
                        # will fail due to no value for the instance argument.
                        try:
                            field_metadata_version = Metadata.__dict__[key].added
                        except KeyError:
                            exc = InvalidMetadata(key, f"unrecognized field: {key!r}")
                            collector.error(exc)
                            continue
                        field_age = _VALID_METADATA_VERSIONS.index(
                            field_metadata_version
                        )
                        if field_age > metadata_age:
                            field = _RAW_TO_EMAIL_MAPPING[key]
                            exc = InvalidMetadata(
                                field,
                                f"{field} introduced in metadata version "
                                f"{field_metadata_version}, not {metadata_version}",
                            )
                            collector.error(exc)
                            continue
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
            # Make sure to check for the fields that are present, the required
            # fields (so their absence can be reported).
            fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
            # Remove fields that have already been checked.
            fields_to_check -= {"metadata_version"}

            fields_ok: set[str] = set()
            for key in fields_to_check:
                try:
                    if metadata_version:
                        # Can't use getattr() as that triggers descriptor protocol which
                        # will fail due to no value for the instance argument.
                        try:
                            field_metadata_version = Metadata.__dict__[key].added
                        except KeyError:
                            exc = InvalidMetadata(key, f"unrecognized field: {key!r}")
                            collector.error(exc)
                            continue
                        field_age = _VALID_METADATA_VERSIONS.index(
                            field_metadata_version
                        )
                        if field_age > metadata_age:
                            field = _RAW_TO_EMAIL_MAPPING[key]
                            exc = InvalidMetadata(
                                field,
                                f"{field} introduced in metadata version "
                                f"{field_metadata_version}, not {metadata_version}",
                            )
                            collector.error(exc)
                            continue
                    getattr(ins, key)
                    fields_ok.add(key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            if "provides_extra" in fields_ok and "requires_dist" in fields_ok:
                provides_extra = ins.provides_extra
                if provides_extra is not None:
                    for exc in _check_undeclared_extras(
                        ins.requires_dist, provides_extra
                    ):
                        collector.error(exc)

            collector.finalize("invalid metadata")
>>>>>>> REPLACE