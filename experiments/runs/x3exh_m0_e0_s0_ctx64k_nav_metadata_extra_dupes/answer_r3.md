### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            provided_extras = ins.__dict__.get("provides_extra")
            reqs = ins.__dict__.get("requires_dist")
            if provided_extras is not None and reqs is not None:
                declared = set(provided_extras)
                for req in reqs:
                    if req.marker is not None:
                        raw_extras = _extract_extras_from_markers(
                            req.marker._markers
                        )
                        for extra in raw_extras:
                            if utils.canonicalize_name(extra) not in declared:
                                collector.error(
                                    InvalidMetadata(
                                        "requires-dist",
                                        f"{extra!r} is not declared in provides-extra",
                                    )
                                )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE