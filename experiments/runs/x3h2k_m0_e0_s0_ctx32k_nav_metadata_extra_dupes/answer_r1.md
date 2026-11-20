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
        normalized_names = []
        seen = set()
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra {canonical!r} in {self.raw_name!r}",
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
  return cast("RawMetadata", raw), unparsed
=======
  return cast("RawMetadata", raw), unparsed


def _get_extra_names_from_marker(
    marker: markers.MarkerList | markers.MarkerAtom,
) -> set[str]:
    extras: set[str] = set()
    if isinstance(marker, list):
        for item in marker:
            extras |= _get_extra_names_from_marker(item)
    elif isinstance(marker, tuple):
        lhs, op, rhs = marker
        if isinstance(lhs, list):
            # MarkerLogical: recurse into lhs and rhs (which are lists)
            extras |= _get_extra_names_from_marker(lhs)
            extras |= _get_extra_names_from_marker(rhs)
        else:
            # MarkerAtom: check for extra comparisons
            if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                if isinstance(rhs, markers.Value):
                    extras.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                if isinstance(lhs, markers.Value):
                    extras.add(utils.canonicalize_name(lhs.value))
    return extras
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")
=======
                  except InvalidMetadata as exc:
                      collector.error(exc)

              # Check for undeclared extras in requires_dist
              has_provides_extra_error = any(
                  isinstance(e, InvalidMetadata) and e.field == "provides-extra"
                  for e in collector.errors
              )
              has_requires_dist_error = any(
                  isinstance(e, InvalidMetadata) and e.field == "requires-dist"
                  for e in collector.errors
              )

              if not has_provides_extra_error and not has_requires_dist_error:
                  provides_extra = ins.provides_extra
                  requires_dist = ins.requires_dist
                  if provides_extra is not None and requires_dist is not None:
                      for req in requires_dist:
                          if req.marker is not None:
                              extra_names = _get_extra_names_from_marker(req.marker.markers)
                              for extra_name in extra_names:
                                  if extra_name not in provides_extra:
                                      collector.error(
                                          InvalidMetadata(
                                              "requires-dist",
                                              f"extra {extra_name!r} in requirement {req.name!r} is not declared in provides-extra",
                                          )
                                      )

              collector.finalize("invalid metadata")
>>>>>>> REPLACE