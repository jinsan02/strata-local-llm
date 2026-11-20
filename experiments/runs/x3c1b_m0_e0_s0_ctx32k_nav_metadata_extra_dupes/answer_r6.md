수정 내용을 설명합니다.
1. `_process_provides_extra` 메서드에서 정규화된 이름을 추가할 때 중복을 검사하여 `InvalidMetadata`를 발생하도록 변경했습니다.
2. 모듈 레벨에 `_check_undeclared_extras` 함수와 마커 트리를 순회해 `extra == "값"` 형태를 추출하는 `_extract_extra_values` 헬퍼를 추가했습니다.
3. `Metadata.from_raw`에서 검증 루프가 `_raw`를 비우기 전에 원본 값을 미리 저장하고, 모든 필드 검증이 끝난 후 undeclared extra 검사를 수행하도록 수정했습니다.

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
            try:
                for name in value:
                    canonicalized = utils.canonicalize_name(name, validate=True)
                    if canonicalized in normalized_names:
                        raise self._invalid_metadata(
                            f"duplicate value {canonicalized!r} in {self.raw_name!r}"
                        )
                    normalized_names.append(canonicalized)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            else:
                return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
class Metadata:
=======
from packaging import markers
from packaging._parser import Variable, Value


def _extract_extra_values(marker_list) -> set[utils.NormalizedName]:
    """Extract canonicalized extra values from marker equality comparisons."""
    result: set[utils.NormalizedName] = set()
    if not isinstance(marker_list, list):
        return result
    for item in marker_list:
        if isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            val = None
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    val = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    val = lhs.value
            if val is not None:
                result.add(utils.canonicalize_name(val))
        else:
            result.update(_extract_extra_values(item))
    return result


def _check_undeclared_extras(
    requires_dist: list[str],
    provides_extra: list[str] | None,
    collector: "_ErrorCollector",
) -> None:
    """Validate that extras used in markers are declared in provides-extra."""
    if provides_extra is None:
        return

    provided_set: set[utils.NormalizedName] = set()
    for name in provides_extra:
        try:
            provided_set.add(utils.canonicalize_name(name, validate=True))
        except utils.InvalidName:
            # If provides-extra itself is malformed, skip the check as instructed
            return

    for req_str in requires_dist:
        semi_idx = req_str.find(";")
        marker_str = req_str[semi_idx + 1:] if semi_idx != -1 else ""
        if not marker_str:
            continue

        try:
            m = markers.Marker(marker_str)
        except markers.InvalidMarker:
            # Skip syntactically invalid markers; they will be caught elsewhere
            continue

        declared_extras = _extract_extra_values(m.marker)
        for extra in declared_extras:
            if extra not in provided_set:
                collector.error(InvalidMetadata("requires-dist", f"extra {extra!r} is not declared in provides-extra"))


class Metadata:
>>>>>>> REPLACE
<<<<<<< SEARCH
          ins._raw = data.copy()  # Mutations occur due to caching enriched values.

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
          ins._raw = data.copy()  # Mutations occur due to caching enriched values.

          if validate:
              # Capture raw lists early because _Validator.__get__ pops keys from _raw
              raw_requires = ins._raw.get("requires_dist")
              raw_provides = ins._raw.get("provides_extra")

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

              # Check undeclared extras after individual field validations
              if raw_requires is not None and raw_provides is not None:
                  _check_undeclared_extras(raw_requires, raw_provides, collector)

              collector.finalize("invalid metadata")
>>>>>>> REPLACE