### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
=======
class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class InvalidGroupName(ValueError):
    """
    An invalid dependency group name was provided.

    Dependency group names must follow the same rules as core metadata
    :pep:`345#name`.

    .. versionadded:: 26.x
    """

    def __init__(self, name: str) -> None:
        super().__init__(f"name is invalid: {name!r}")


class CyclicDependencyGroup(ValueError):
>>>>>>> REPLACE