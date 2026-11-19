### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE
<<<<<<< SEARCH
      def evaluate_prepared(
          self, environment: Mapping[str, str | AbstractSet[str]]
      ) -> bool:
=======
      def referenced_extras(self) -> frozenset[NormalizedName]:
          """Return all extra names referenced in this marker.

          Extracts names from comparisons like ``extra == "Foo"`` or
          membership checks like ``"Foo" in extras``, returning them as a
          normalized ``frozenset``. Only ``extra`` variables and set-valued
          markers (like ``extras``) are considered; other environment keys
          are ignored.
          """
          results: set[str] = set()

          def _visit(node: MarkerAtom | MarkerLogical) -> None:
              if isinstance(node, list):
                  for item in node:
                      if item not in ("and", "or"):
                          _visit(item)
                  return
              
              # Comparison tuple: (lhs, op, rhs)
              lhs, _, rhs = node
              
              # Direct extra comparisons: extra == "value" or "value" == extra
              if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                  results.add(canonicalize_name(rhs.value))
              elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                  results.add(canonicalize_name(lhs.value))
              
              # Set membership: "value" in extras / "value" in dependency_groups
              if isinstance(rhs, Variable) and rhs.value in MARKERS_ALLOWING_SET and isinstance(lhs, Value):
                  results.add(canonicalize_name(lhs.value))

          _visit(self._markers)
          return frozenset(results)

      def evaluate_prepared(
          self, environment: Mapping[str, str | AbstractSet[str]]
      ) -> bool:
>>>>>>> REPLACE
<<<<<<< SEARCH
  from typing import TYPE_CHECKING, Any

  from ._parser import parse_requirement as _parse_requirement
=======
  from typing import TYPE_CHECKING, Any
  
  from collections.abc import Mapping as CollectionMapping

  from ._parser import MarkerList, parse_requirement as _parse_requirement
>>>>>>> REPLACE
<<<<<<< SEARCH
      def __init__(self, requirement_string: str) -> None:
=======
      @property
      def marker_extras(self) -> frozenset[str]:
          """Extract extra names referenced in this requirement's marker."""
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()

      def __init__(self, requirement_string: str) -> None:
>>>>>>> REPLACE