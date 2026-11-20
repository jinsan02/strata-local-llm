### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras
            if validate:
                try:
                    provided_extras = ins.provides_extra
                    requires_dist = ins.requires_dist
                except InvalidMetadata:
                    pass
                else:
                    if provided_extras is not None:
                        from packaging._parser import Variable
                        
                        for req in requires_dist:
                            if req.marker is not None:
                                def _find_extras(tree):
                                    extras = []
                                    for node in tree:
                                        if isinstance(node, str):
                                            continue
                                        if isinstance(node, tuple):
                                            left, op, right = node
                                            if isinstance(left, Variable) and left.value == "extra" and op.value == "==":
                                                extras.append(right.value)
                                            elif isinstance(right, Variable) and right.value == "extra" and op.value == "==":
                                                extras.append(left.value)
                                        elif isinstance(node, list):
                                            extras.extend(_find_extras(node))
                                    return extras
                                
                                for extra_name in _find_extras(req.marker._markers):
                                    if utils.canonicalize_name(extra_name) not in provided_extras:
                                        raise InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra_name!r} not found in Provides-Extra"
                                        )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE