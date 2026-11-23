### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
            collector.finalize("invalid metadata")

        return ins
=======
            # Check for undeclared extras in requires-dist markers
            if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__:
                provides_extra = ins.__dict__["provides_extra"]
                requires_dist = ins.__dict__["requires_dist"]
                if provides_extra is not None:
                    declared_extras = set(provides_extra)
                    undeclared_extras = set()
                    if requires_dist:
                        from . import _parser
                        for req in requires_dist:
                            if req.marker:
                                _extract_marker_extras(
                                    req.marker._markers,
                                    undeclared_extras,
                                    _parser,
                                )
                    for extra in sorted(undeclared_extras):
                        if utils.canonicalize_name(extra) not in declared_extras:
                            collector.error(
                                InvalidMetadata(
                                    "requires-dist",
                                    f"extra {extra!r} in requires-dist is not declared in provides-extra",
                                )
                            )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE