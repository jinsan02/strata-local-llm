<tool_call>
<function=edit_file>
<parameter=new_string>
from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
from .utils import InvalidName, canonicalize_name


def _validate_name(name: str) -> None:
    """Validate a dependency group name using the core metadata Name rules."""
    try:
        canonicalize_name(name, validate=True)
    except InvalidName as exc:
        raise InvalidGroupName(f"Invalid dependency group name: {name!r}") from exc


def _normalize_group_names(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    errors: _ErrorCollector,
) -> dict[str, Sequence[str | Mapping[str, str]]]:
    original_names: dict[str, list[str]] = {}
    normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

    for group_name, value in dependency_groups.items():
        try:
            canonicalize_name(group_name, validate=True)
        except InvalidName as exc:
            errors.error(InvalidGroupName(f"Invalid dependency group name: {group_name!r}"))
        
        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value

    for normed_name, names in original_names.items():
        if len(names) > 1:
            errors.error(
                DuplicateGroupNames(
                    "Duplicate dependency group names: "
                    f"{normed_name} ({', '.join(names)})"
                )
            )

    return normalized_groups
</parameter>
<parameter=old_string>
from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
from .utils import InvalidName, canonicalize_name, is_normalized_name


def _validate_name(name: str) -> None:
    """Validate a dependency group name using the same rules as PEP 503 names."""
    if not is_normalized_name(name):
        raise InvalidGroupName(f"Invalid dependency group name: {name!r}")

__all__ = [
    "CyclicDependencyGroup",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "DuplicateGroupNames",
    "InvalidGroupName",
    "InvalidDependencyGroupObject",
    "resolve_dependency_groups",
]


def __dir__() -> list[str]:
    return __all__


# -----------
# Error Types
# -----------


class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class InvalidGroupName(ValueError):
    """
    A dependency group name did not follow the PEP 503 / core metadata Name rules.

    .. versionadded:: 26.2
    """


class CyclicDependencyGroup(ValueError):
</parameter>
<parameter=path>
src/packaging/dependency_groups.py
</parameter>
</function>
</tool_call>