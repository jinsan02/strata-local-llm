### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    TypeVar,
)
=======
from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    Optional,
    Tuple,
    TypeVar,
)
>>>>>>> REPLACE

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
_Bound = Tuple[Version, bool]


def _specifier_bounds(spec: Specifier) -> Tuple[Optional[_Bound], Optional[_Bound]]:
    op = spec.operator
    ver_str = spec.version
    
    if op == "===":
        raise ValueError("=== operator is not supported for bounds()")
        
    v = spec._require_spec_version()
    
    if op == ">=":
        return ((v, True), None)
    if op == ">":
        return ((v, False), None)
    if op == "<=":
        return (None, (v, True))
    if op == "<":
        return (None, (v, False))
    if op == "==":
        if ver_str.endswith(".*"):
            lower = (v, True)
            new_release = (*v.release[:-1], v.release[-1] + 1)
            upper_v = Version.from_parts(epoch=v.epoch, release=new_release)
            return (lower, (upper_v, False))
        return ((v, True), (v, True))
    if op == "~=":
        lower = (v, True)
        new_release = (*v.release[:-2], v.release[-2] + 1)
        upper_v = Version.from_parts(epoch=v.epoch, release=new_release)
        return (lower, (upper_v, False))
    if op == "!=":
        return (None, None)
        
    raise ValueError(f"Unknown operator: {op!r}")


def _combine_bounds(
    low1: Optional[_Bound], high1: Optional[_Bound],
    low2: Optional[_Bound], high2: Optional[_Bound]
) -> Tuple[Optional[_Bound], Optional[_Bound]]:
    if low1 is None:
        combined_low = low2
    elif low2 is None:
        combined_low = low1
    else:
        v1, inc1 = low1
        v2, inc2 = low2
        if v1 > v2:
            combined_low = low1
        elif v2 > v1:
            combined_low = low2
        else:
            combined_low = (v1, inc1 and inc2)
            
    if high1 is None:
        combined_high = high2
    elif high2 is None:
        combined_high = high1
    else:
        v1, inc1 = high1
        v2, inc2 = high2
        if v1 < v2:
            combined_high = high1
        elif v2 < v1:
            combined_high = high2
        else:
            combined_high = (v1, inc1 and inc2)
            
    return combined_low, combined_high


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
        return VersionRange._from_specifier_set(self)

    def _check_relation_operand(self, other: object) -> None:
=======
        return VersionRange._from_specifier_set(self)

    def bounds(self) -> tuple[Optional[tuple[Version, bool]], Optional[tuple[Version, bool]]]:
        """Return the combined lower and upper bounds of the specifier set.

        Returns a tuple ``(lower, upper)`` where each element is either
        ``None`` (unbounded) or a ``(Version, inclusive)`` tuple.
        ``lower`` is the maximum of all lower bounds, ``upper`` is the minimum
        of all upper bounds. If versions are equal, an exclusive bound
        (``inclusive=False``) takes precedence over an inclusive one.

        Raises :exc:`ValueError` if any specifier uses the ``===`` operator.
        Prerelease settings do not affect the result.

        >>> SpecifierSet(">=1.0,<2.0").bounds()
        ((Version('1.0'), True), (Version('2.0'), False))
        >>> SpecifierSet("==1.0").bounds()
        ((Version('1.0'), True), (Version('1.0'), True))
        >>> SpecifierSet("~=1.4").bounds()
        ((Version('1.4'), True), (Version('2.0'), False))
        >>> SpecifierSet(">=1.0").bounds()
        ((Version('1.0'), True), None)
        >>> SpecifierSet("").bounds()
        (None, None)
        """
        if self._has_arbitrary:
            raise ValueError("=== operator is not supported for bounds()")
            
        lower: Optional[tuple[Version, bool]] = None
        upper: Optional[tuple[Version, bool]] = None
        
        for spec in self._specs:
            spec_low, spec_high = _specifier_bounds(spec)
            lower, upper = _combine_bounds(lower, upper, spec_low, spec_high)
            
        return lower, upper

    def _check_relation_operand(self, other: object) -> None:
>>>>>>> REPLACE