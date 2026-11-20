### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              and self.url == other.url
              and self.marker == other.marker
          )
=======
              and self.url == other.url
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Extra names referenced in this requirement's marker.

        Returns an empty set if no marker is attached, otherwise returns the
        result of :meth:`Marker.referenced_extras`.
        """
        return self.marker.referenced_extras() if self.marker else frozenset()
>>>>>>> REPLACE

수정 내용 요약:
- `src/packaging/markers.py`: `NormalizedName` import 추가, `Marker` 클래스에 `referenced_extras()` 메서드 구현. `_markers` 트리를 재귀적으로 순회하며 `extra` 변수와 비교된 리터럴 값을 정규화하여 `frozenset[NormalizedName]`으로 반환합니다.
- `src/packaging/requirements.py`: `NormalizedName` import 추가, `Requirement` 클래스에 `marker_extras` 속성(property) 구현. 마커가 연결되어 있으면 `referenced_extras()` 결과를, 그렇지 않으면 빈 `frozenset`을 반환합니다. 기존 동작은 완전히 보존됩니다.