EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    from . import licenses, requirements, specifiers, utils
    from . import version as version_module
=======
    from . import licenses, requirements, specifiers, utils
    from . import version as version_module
    from ._parser import Variable, Value
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
                          f"Duplicate provides-extra {name!r}"
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
  _REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


class _Validator(Generic[T]):
=======
  _REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


def _find_extras_in_markers(marker_tree):
    """Extract extra names from a parsed marker tree structure."""
    extras = set()
    if isinstance(marker_tree, tuple):
        lhs, op, rhs = marker_tree
        if isinstance(lhs, Variable) and lhs.value == "extra":
            if isinstance(rhs, Value):
                extras.add(rhs.value)
        elif isinstance(rhs, Variable) and rhs.value == "extra":
            if isinstance(lhs, Value):
                extras.add(lhs.value)
    elif isinstance(marker_tree, list):
        for item in marker_tree:
            extras.update(_find_extras_in_markers(item))
    return extras


class _Validator(Generic[T]):
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")
=======
                  except InvalidMetadata as exc:
                      collector.error(exc)

              # Check for undeclared extras in requires_dist markers
              try:
                  provided_extras = getattr(ins, "provides_extra")
                  requires_dist = getattr(ins, "requires_dist")
              except InvalidMetadata:
                  provided_extras = None
                  requires_dist = None

              if provided_extras is not None and requires_dist is not None:
                  provided_set = set(provided_extras)
                  for req in requires_dist:
                      marker = req.marker
                      if marker is not None:
                          extra_names = _find_extras_in_markers(marker._markers)
                          for extra in extra_names:
                              if extra not in provided_set:
                                  collector.error(InvalidMetadata(
                                      "requires-dist",
                                      f"Extra {extra!r} is not specified."
                                  ))

              collector.finalize("invalid metadata")
>>>>>>> REPLACE