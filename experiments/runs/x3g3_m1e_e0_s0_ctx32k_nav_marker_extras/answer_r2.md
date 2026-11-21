### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this marker.

        Scans the entire marker expression (including ``and``/``or`` chains and
        parenthesised sub-expressions) for every comparison involving the
        ``extra`` variable or the ``extras`` set.  The returned names are
        canonicalised (PEP 503).

        >>> from packaging.markers import Marker
        >>> Marker('extra == "dev" or python_version > "3.6"').referenced_extras()
        frozenset({'dev'})
        >>> Marker('extra == "A" and extra == "B"').referenced_extras()
        frozenset({'a', 'b'})
        >>> Marker('sys_platform == "linux"').referenced_extras()
        frozenset()

        .. versionadded:: 26.5
        """
        extras: set[str] = set()
        self._collect_extras(self._markers, extras)
        return frozenset(extras)

    @staticmethod
    def _collect_extras(
        markers: MarkerList, extras: set[str]
    ) -> None:
        """Recursively walk *markers* and collect every extra name into *extras*."""
        for item in markers:
            if isinstance(item, list):
                Marker._collect_extras(item, extras)
            elif isinstance(item, tuple):
                lhs, _op, rhs = item
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.add(lhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extras":
                    if isinstance(lhs, Value):
                        extras.add(lhs.value)
                elif isinstance(lhs, Variable) and lhs.value == "extras":
                    if isinstance(rhs, Value):
                        extras.add(rhs.value)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        raise TypeError(f"Cannot restore Requirement from {state!r}")
=======
        raise TypeError(f"Cannot restore Requirement from {state!r}")

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in the requirement's marker.

        If there is no marker, returns an empty :class:`frozenset`.
        Otherwise, delegates to :meth:`Marker.referenced_extras`.

        >>> from packaging.requirements import Requirement
        >>> Requirement('foo[extra1] ; extra == "extra2"').marker_extras
        frozenset({'extra2'})
        >>> Requirement('bar').marker_extras
        frozenset()

        .. versionadded:: 26.5
        """
        return self.marker.referenced_extras() if self.marker is not None else frozenset()
>>>>>>> REPLACE

`NormalizedName`는 `packaging.utils`에서 `str`의 별칭이므로 타입 힌트는 `str`로 통일해 불필요한 import를 피했습니다. `Marker`에 재귀 탐색 메서드를, `Requirement`에 위임을 위한 property를 추가했으며 기존 문자열화/해시/평가 로직은 건드리지 않았습니다.