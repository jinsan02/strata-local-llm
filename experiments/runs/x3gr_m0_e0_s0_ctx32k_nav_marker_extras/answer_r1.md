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
        """Return all extra names referenced in the marker.

        If the requirement has no marker, returns an empty frozenset.
        Otherwise, returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE

수정 완료. `packaging.markers.Marker`에 `referenced_extras()` 메서드를, `packaging.requirements.Requirement`에 `marker_extras` 속성을 추가했습니다. 기존 동작은 변경되지 않았습니다.