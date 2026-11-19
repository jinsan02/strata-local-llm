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
                canonicalized = utils.canonicalize_name(name, validate=True)
                if canonicalized in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra name {name!r} found"
                    )
                seen.add(canonicalized)
                normalized_names.append(canonicalized)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
              collector.error(exc)

              collector.finalize("invalid metadata")

          return ins
=======
              collector.error(exc)

              # Check undeclared extras in requires_dist
              provided_extras = ins.__dict__.get("provides_extra")
              reqs = ins.__dict__.get("requires_dist")
              if provided_extras is not None and reqs is not None:
                  extra_re = re.compile(
                      r"""['"](?P<val>[^'"]+)['"]\s*==\s*(?:"extra"|'extra')|(?:"extra"|'extra')\s*==\s*['"](?P<val>[^'"]+)['"]""", 
                      re.IGNORECASE
                  )
                  raw_reqs = ins._raw.get("requires_dist")
                  if raw_reqs:
                      for raw_req in raw_reqs:
                          if ";" in raw_req:
                              marker_str = raw_req.split(";", 1)[1].strip()
                              for match in extra_re.finditer(marker_str):
                                  val = match.group("val")
                                  canonical_val = utils.canonicalize_name(val, validate=False)
                                  if canonical_val not in provided_extras:
                                      collector.error(
                                          InvalidMetadata(
                                              "requires-dist",
                                              f"extra {val!r} is not declared in provides-extra"
                                          )
                                      )

              collector.finalize("invalid metadata")

          return ins
>>>>>>> REPLACE