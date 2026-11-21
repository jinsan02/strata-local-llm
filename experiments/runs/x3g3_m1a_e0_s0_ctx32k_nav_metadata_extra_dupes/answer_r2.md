### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from ._parser import Variable, Value
from .errors import ExceptionGroup, _ErrorCollector
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
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in normalized_names:
                    raise self._invalid_metadata(
                        f"duplicate extra {normalized!r} in {self.raw_name!r}"
                    )
                normalized_names.append(normalized)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _extract_extra_names(marker: list) -> set[str]:
    extras: set[str] = set()
    for item in marker:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.update(_extract_extra_names(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if op.serialize() in ("==", "!="):
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.add(lhs.value)
    return extras


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check undeclared extras in requires_dist markers
            if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__:
                provides_extra = ins.__dict__["provides_extra"]
                requires_dist = ins.__dict__["requires_dist"]
                if provides_extra is not None:
                    declared = set(provides_extra)
                    for req in requires_dist:
                        if req.marker:
                            for extra in _extract_extra_names(req.marker):
                                if extra not in declared:
                                    collector.error(
                                        InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra!r} in requires-dist is not in provides-extra"
                                        )
                                    )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE

수정 요약:
1. `_process_provides_extra` 메서드에서 정규화된 이름이 중복되면 `InvalidMetadata` 예외를 던지도록 변경했습니다.
2. `_extract_extra_names` 헬퍼 함수를 추가하여 마커 트리에서 `extra == "값"` 또는 `"값" == extra` 비교에서 참조된 extra 이름을 추출합니다.
3. `from_raw` 검증 로직에서 `provides_extra`와 `requires_dist`가 모두 성공적으로 처리된 경우, 마커에 등장하는 extra가 `provides_extra`에 선언되어 있는지 검증합니다. 누락된 경우 `requires-dist` 필드 이름으로 `InvalidMetadata` 오류를 수집하여 `ExceptionGroup`으로 함께 반환합니다. `validate=False`일 때는 이 검사가 실행되지 않으며, 기존 동작은 유지됩니다.