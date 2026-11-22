### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _parse_project_urls(data: list[str]) -> dict[str, str]:
=======
def _get_extra_values_from_marker(markers: list) -> set[utils.NormalizedName]:
    """Extract normalized extra names from a parsed marker tree."""
    extras: set[utils.NormalizedName] = set()
    for item in markers:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.update(_get_extra_values_from_marker(item))
        elif isinstance(item, tuple):
            lhs, _, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(lhs.value)
    return extras


def _parse_project_urls(data: list[str]) -> dict[str, str]:
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
        normalized_names: list[utils.NormalizedName] = []
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"{normalized!r} is a duplicate for {self.raw_name!r}"
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
<<<<<<< SEARCH
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")

          return ins
=======
                  except InvalidMetadata as exc:
                      collector.error(exc)

              # Check for undeclared extras in requires_dist markers
              try:
                  provides_extra = ins.provides_extra
                  requires_dist = ins.requires_dist
              except InvalidMetadata:
                  pass
              else:
                  if provides_extra is not None and requires_dist is not None:
                      declared = set(provides_extra)
                      for req in requires_dist:
                          if req.marker is not None:
                              found_extras = _get_extra_values_from_marker(req.marker._markers)
                              for extra in found_extras:
                                  if extra not in declared:
                                      collector.error(InvalidMetadata(
                                          "requires-dist",
                                          f"extra {extra!r} is not declared in provides-extra"
                                      ))

              collector.finalize("invalid metadata")

          return ins
>>>>>>> REPLACE