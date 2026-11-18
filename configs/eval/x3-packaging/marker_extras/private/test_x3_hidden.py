import pytest

from packaging.markers import Marker
from packaging.requirements import Requirement


@pytest.mark.parametrize(
    ("marker", "expected"),
    [
        ('extra == "Test_Foo"', {"test-foo"}),
        ('"Docs" == extra', {"docs"}),
        ('extra != "a.b"', {"a-b"}),
        ('python_version >= "3.8" and (extra == "x" or extra == "Y")', {"x", "y"}),
        ('"Foo" in extras', {"foo"}),
        ('"bar" not in extras and os_name == "nt"', {"bar"}),
        ('os_name == "nt"', set()),
        ('"dev" in dependency_groups', set()),
        ('(extra == "a" and (extra == "b" or "c" in extras))', {"a", "b", "c"}),
    ],
)
def test_referenced_extras(marker, expected):
    result = Marker(marker).referenced_extras()
    assert isinstance(result, frozenset)
    assert result == frozenset(expected)


def test_combined_markers():
    m = (Marker('extra == "a"') & Marker('os_name == "nt"')) | Marker('extra == "B"')
    assert m.referenced_extras() == {"a", "b"}


def test_requirement_marker_extras():
    assert Requirement('foo[bar]; extra == "Baz"').marker_extras == {"baz"}
    assert Requirement("foo>=1").marker_extras == frozenset()
    assert isinstance(Requirement("foo").marker_extras, frozenset)
    assert Requirement('foo; "X" in extras or extra == "y"').marker_extras == {"x", "y"}
