수정이 완료되었습니다. 주요 변경 사항:

1. `_process_provides_extra` 메서드에 중복 검사 추가 (`seen` set 사용)
2. `_extract_extra_values_from_markers` 헬퍼 함수 추가 (마커에서 `extra == "name"` 비교에서 extra 이름 추출)
3. `from_raw` 메서드에 undeclared extra 검사 추가 (`validate=True`일 때만, `provides_extra`/`requires_dist` 유효할 때만)

```python
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
>>>>>>> REPLACE
```

```python
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
                        f"duplicate {self.raw_name!r} value {normalized!r}"
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
```

```python
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _extract_extra_values_from_markers(
    markers: markers.MarkerList,
) -> set[str]:
    """Extract extra names from marker expressions that compare `extra` with a value.

    Only extracts values from comparisons like `extra == "docs"` or `"docs" == extra`.
    Does not extract from `in` / `not in` comparisons (e.g. `"docs" in extras`).
    Returns a set of canonicalized extra names.
    """
    result: set[str] = set()

    def _extract(node: markers.MarkerAtom) -> None:
        if isinstance(node, list):
            for item in node:
                _extract(item)
        elif isinstance(node, str):
            # "and" or "or" — skip
            pass
        elif isinstance(node, tuple):
            lhs, op, rhs = node
            # Check if this is an `extra` comparison (not `in`/`not in`)
            if op.serialize() in {"==", "!="}:
                if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                    if isinstance(rhs, markers.Value):
                        result.add(utils.canonicalize_name(rhs.value))
                elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                    if isinstance(lhs, markers.Value):
                        result.add(utils.canonicalize_name(lhs.value))

    _extract(markers)
    return result


class Metadata:
>>>>>>> REPLACE
```

```python
<<<<<<< SEARCH
          if validate:
              collector = _ErrorCollector()
              metadata_version = None
              with collector.collect(InvalidMetadata):
                  metadata_version = ins.metadata_version
                  metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

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
          if validate:
              collector = _ErrorCollector()
              metadata_version = None
              with collector.collect(InvalidMetadata):
                  metadata_version = ins.metadata_version
                  metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

              # Make sure to check for the fields that are present, the required
              # fields (so their absence can be reported).
              fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
              # Remove fields that have already been checked.
              fields_to_check -= {"metadata_version"}

              provides_extra_ok = True
              requires_dist_ok = True
              # Store raw values before the loop, since accessing properties
              # removes them from _raw.
              raw_provides_extra = ins._raw.get("provides_extra")
              raw_requires_dist = ins._raw.get("requires_dist")
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
                      if exc.field == "provides-extra":
                          provides_extra_ok = False
                      elif exc.field == "requires-dist":
                          requires_dist_ok = False

              # Check for undeclared extras in requires_dist markers.
              if provides_extra_ok and requires_dist_ok:
                  if raw_provides_extra is not None and raw_requires_dist is not None:
                      # Get the canonicalized provides_extra set
                      canonical_provides = set(ins.provides_extra)
                      # Extract extra names from requires_dist markers
                      declared_extras: set[str] = set()
                      for req_str in raw_requires_dist:
                          try:
                              req = requirements.Requirement(req_str)
                              if req.marker is not None:
                                  declared_extras.update(
                                      _extract_extra_values_from_markers(req.marker._markers)
                                  )
                          except requirements.InvalidRequirement:
                              # If the requirement itself is invalid, skip this one.
                              continue
                      for extra_name in declared_extras:
                          if extra_name not in canonical_provides:
                              collector.error(
                                  InvalidMetadata(
                                      "requires-dist",
                                      f"extra {extra_name!r} not found in provides_extra",
                                  )
                              )

              collector.finalize("invalid metadata")
>>>>>>> REPLACE
```