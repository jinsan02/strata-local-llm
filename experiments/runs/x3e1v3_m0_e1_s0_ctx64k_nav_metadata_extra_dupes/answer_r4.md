<tool_call>
<function=edit_file>
<parameter=path>
src/packaging/metadata.py
</parameter>
<parameter=old_string>
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from .licenses import NormalizedLicenseExpression
    from .version import Version

T = typing.TypeVar("T")
</parameter>
<parameter=new_string>
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from .licenses import NormalizedLicenseExpression
    from .version import Version
    from ._parser import MarkerAtom, MarkerList, MarkerLogical, Op, Value, Variable

T = typing.TypeVar("T")


def _extract_extra_values(markers: MarkerList) -> set[utils.NormalizedName]:
    """Extract canonicalized extra names from marker expressions.

    Finds all comparisons of the form `extra == "name"` or `"name" == extra`
    (with `==` or `!=` operators) and returns the set of canonicalized extra
    names. Does not follow `and`/`or`/parentheses boundaries.
    """
    result: set[utils.NormalizedName] = set()

    def _visit(node: MarkerAtom | MarkerLogical) -> None:
        if isinstance(node, str):
            # "and" or "or" - skip, we don't need to follow logical operators
            return
        if isinstance(node, list):
            for item in node:
                _visit(item)
            return
        # It's a tuple: (lhs, op, rhs)
        lhs, op, rhs = node  # type: ignore[misc]
        op_str = op.serialize() if isinstance(op, Op) else str(op)
        if op_str not in ("==", "!="):
            return

        # Check if this is an extra comparison
        extra_value: str | None = None
        if isinstance(lhs, Variable) and lhs.value == "extra":
            if isinstance(rhs, Value):
                extra_value = rhs.value
        elif isinstance(rhs, Variable) and rhs.value == "extra":
            if isinstance(lhs, Value):
                extra_value = lhs.value

        if extra_value is not None:
            result.add(utils.canonicalize_name(extra_value))

    for item in markers:
        _visit(item)

    return result
</parameter>
</function>
</tool_call>