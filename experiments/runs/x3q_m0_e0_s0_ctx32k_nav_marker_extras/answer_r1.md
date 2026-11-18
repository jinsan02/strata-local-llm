### 편집 블록

`packaging/markers.py` 파일에 `NormalizedName` 타입을 import 하고, `Marker` 클래스에 `referenced_extras()` 메서드를 추가합니다.

```python
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE
```

```python
<<<<<<< SEARCH
      def evaluate_prepared(
          self, environment: Mapping[str, str | AbstractSet[str]]
      ) -> bool:
=======
      def referenced_extras(self) -> frozenset[NormalizedName]:
          """Return a ``frozenset`` of canonicalized extra names referenced by this marker."""
          def _collect(node: MarkerAtom | MarkerLogical) -> set[NormalizedName]:
              extras: set[NormalizedName] = set()
              if isinstance(node, str):
                  return extras
              if isinstance(node, tuple):
                  lhs, op, rhs = node
                  if isinstance(lhs, Variable) and lhs.value == "extra":
                      if isinstance(rhs, Value):
                          extras.add(canonicalize_name(rhs.value))
                  elif isinstance(rhs, Variable) and rhs.value == "extra":
                      if isinstance(lhs, Value):
                          extras.add(canonicalize_name(lhs.value))
              else:
                  for item in node:
                      extras |= _collect(item)
              return extras

          return frozenset(_collect(self._markers))

      def evaluate_prepared(
          self, environment: Mapping[str, str | AbstractSet[str]]
      ) -> bool:
>>>>>>> REPLACE
```

`packaging/requirements.py` 파일에 `NormalizedName` 타입을 import 하고, `Requirement` 클래스에 `marker_extras` 속성(property)을 추가합니다.

```python
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE
```

```python
<<<<<<< SEARCH
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )
=======
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return the extra names referenced in the marker, or an empty frozenset."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE
```