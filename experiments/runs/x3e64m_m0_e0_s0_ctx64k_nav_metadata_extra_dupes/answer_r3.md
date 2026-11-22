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
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"Duplicate extra: {name!r}",
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
<<<<<<< SEARCH
              collector.finalize("invalid metadata")

          return ins
=======
              collector.finalize("invalid metadata")

              # Check for undefined extras in requires_dist markers
              # This check requires both provides_extra and requires_dist to be valid
              provides_extra_valid = (
                  "provides_extra" in ins.__dict__
                  and "provides_extra" not in ins._raw
              )
              requires_dist_valid = (
                  "requires_dist" in ins.__dict__
                  and "requires_dist" not in ins._raw
              )

              if provides_extra_valid and requires_dist_valid:
                  provides_extra = ins.__dict__["provides_extra"]
                  requires_dist = ins.__dict__["requires_dist"]

                  if provides_extra is not None:
                      from packaging._parser import Variable, Value

                      for req in requires_dist:
                          marker_str = req.marker
                          if not marker_str:
                              continue

                          try:
                              from packaging import markers

                              marker_obj = markers.Marker(marker_str)
                              # marker_obj.marker is a MarkerList (list of atoms and ops)
                              for item in marker_obj.marker:
                                  if isinstance(item, tuple):
                                      lhs, op, rhs = item
                                      # Check for extra comparisons (extra == "value" or "value" == extra)
                                      is_extra = False
                                      extra_value = None

                                      if (
                                          isinstance(lhs, Variable)
                                          and lhs.value == "extra"
                                          and isinstance(rhs, Value)
                                      ):
                                          is_extra = True
                                          extra_value = rhs.value
                                      elif (
                                          isinstance(rhs, Variable)
                                          and rhs.value == "extra"
                                          and isinstance(lhs, Value)
                                      ):
                                          is_extra = True
                                          extra_value = lhs.value

                                      if is_extra:
                                          op_str = op.serialize()
                                          if op_str in ("==", "!="):
                                              normalized_extra = utils.canonicalize_name(
                                                  extra_value
                                              )
                                              if normalized_extra not in provides_extra:
                                                  collector.error(
                                                      InvalidMetadata(
                                                          "requires-dist",
                                                          f"Extra {extra_value!r} is not defined in provides_extra",
                                                      )
                                                  )
                          except markers.InvalidMarker:
                              # Should not happen if requires_dist is valid
                              pass

          return ins
>>>>>>> REPLACE