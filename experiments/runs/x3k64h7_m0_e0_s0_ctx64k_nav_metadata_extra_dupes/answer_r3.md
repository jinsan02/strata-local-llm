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
        for name in value:
            try:
                normalized = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            if normalized in seen:
                raise self._invalid_metadata(
                    f"duplicate extra name {normalized!r}",
                )
            seen.add(normalized)
            normalized_names.append(normalized)
        return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
              getattr(ins, key)
                  except InvalidMetadata as exc:
                      collector.error(exc)

              collector.finalize("invalid metadata")
=======
              getattr(ins, key)
                  except InvalidMetadata as exc:
                      collector.error(exc)

              # Check for undeclared extras in requires_dist markers
              try:
                  provides_extra_set = set(getattr(ins, "provides_extra") or [])
              except InvalidMetadata:
                  provides_extra_set = None

              if provides_extra_set is not None and "requires_dist" in fields_to_check:
                  try:
                      requires_dist_list = getattr(ins, "requires_dist")
                  except InvalidMetadata:
                      requires_dist_list = None

                  if requires_dist_list is not None:
                      from packaging._parser import Op, Variable, Value

                      def check_extra_comparisons(marker_tree):
                          if isinstance(marker_tree, tuple):
                              lhs, op, rhs = marker_tree
                              if isinstance(op, Op) and op.serialize() == "==":
                                  extra_val = None
                                  if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                                      extra_val = rhs.value
                                  elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                                      extra_val = lhs.value
                                  
                                  if extra_val is not None:
                                      canonical_extra = utils.canonicalize_name(extra_val)
                                      if canonical_extra not in provides_extra_set:
                                          collector.error(InvalidMetadata("requires-dist", f"extra {extra_val!r} is not defined in provides_extra"))
                          elif isinstance(marker_tree, list):
                              for item in marker_tree:
                                  check_extra_comparisons(item)

                      for req in requires_dist_list:
                          if req.marker is not None:
                              check_extra_comparisons(req.marker._markers)

              collector.finalize("invalid metadata")
>>>>>>> REPLACE