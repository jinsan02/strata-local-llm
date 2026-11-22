### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
            elif (
                isinstance(rhs, Variable)
                and rhs.value in MARKERS_ALLOWING_SET
                and isinstance(lhs, Value)
            ):
                result.add(canonicalize_name(lhs.value))
=======
            elif (
                isinstance(rhs, Variable)
                and rhs.value == "extras"
                and isinstance(lhs, Value)
            ):
                result.add(canonicalize_name(lhs.value))
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return the set of extra names referenced in this marker.

        Collects all extra names used in ``extra`` comparisons (e.g.
        ``extra == "foo"``, ``"foo" == extra``) and ``extras`` membership
        checks (e.g. ``"foo" in extras``, ``"foo" not in extras``).
        Names are returned in their canonical (normalized) form.

        :returns: A :class:`frozenset` of normalized extra names.
        """
        return _extract_referenced_extras(self._markers)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            and self.marker == other.marker
        )
=======
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return the set of extra names referenced in this requirement's marker.

        If the requirement has no marker, returns an empty :class:`frozenset`.
        Otherwise, returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE

### 요약
- `src/packaging/markers.py`: `NormalizedName` import 추가, `_extract_referenced_extras` 헬퍼 함수에 `dependency_groups` 제외 처리 반영, `Marker` 클래스에 `referenced_extras()` 메서드 추가.
- `src/packaging/requirements.py`: `NormalizedName` import 추가, `Requirement` 클래스에 `marker_extras` 속성(property) 추가.
- 기존 문자열화, 해시, 비교, 평가 로직은 건드리지 않았습니다.