### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
  def _normalize_extra_values(results: MarkerList) -> MarkerList:
      """
      Normalize extra values.
      """

      return [_normalize_extras(r) for r in results]


    _GROUP_TYPES: Final = (list, tuple)
=======
  def _normalize_extra_values(results: MarkerList) -> MarkerList:
      """
      Normalize extra values.
      """

      return [_normalize_extras(r) for r in results]


  def _extract_extras(markers: list) -> set[str]:
      found: set[str] = set()
      for m in markers:
          if isinstance(m, tuple):
              lhs, op, rhs = m
              if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                  found.add(rhs.value)
              elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                  found.add(lhs.value)
              elif isinstance(lhs, Value) and isinstance(rhs, Variable) and rhs.value == "extras":
                  found.add(lhs.value)
          elif isinstance(m, list):
              found.update(_extract_extras(m))
      return found


  _GROUP_TYPES: Final = (list, tuple)
>>>>>>> REPLACE