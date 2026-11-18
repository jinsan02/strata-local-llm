import pytest

import packaging.dependency_groups as dg
from packaging.dependency_groups import DependencyGroupResolver, DuplicateGroupNames
from packaging.errors import ExceptionGroup


def test_public_exception():
    assert "InvalidGroupName" in dg.__all__
    assert issubclass(dg.InvalidGroupName, ValueError)


@pytest.mark.parametrize("name", ["-dev", "dev-", ".x", "a b", "", "tést"])
def test_invalid_key_reported(name):
    with pytest.raises(ExceptionGroup) as ei:
        DependencyGroupResolver({name: ["requests"]})
    errs = ei.value.exceptions
    assert any(isinstance(e, dg.InvalidGroupName) and repr(name) in str(e) for e in errs)


def test_collected_with_duplicates():
    with pytest.raises(ExceptionGroup) as ei:
        DependencyGroupResolver({"Foo": [], "foo": [], "bad name": []})
    kinds = {type(e) for e in ei.value.exceptions}
    assert dg.InvalidGroupName in kinds
    assert DuplicateGroupNames in kinds


def test_each_invalid_name_reported():
    with pytest.raises(ExceptionGroup) as ei:
        DependencyGroupResolver({"-a": [], "b-": [], "ok": []})
    assert sum(isinstance(e, dg.InvalidGroupName) for e in ei.value.exceptions) == 2


@pytest.mark.parametrize("name", ["Test_Group", "a.b-c", "x", "9"])
def test_valid_names_unchanged(name):
    r = DependencyGroupResolver({name: ["requests>=2"]})
    assert [str(x) for x in r.resolve(name)] == ["requests>=2"]


def test_lookup_and_resolve_reject_invalid():
    r = DependencyGroupResolver({"test": ["pytest"]})
    with pytest.raises(dg.InvalidGroupName):
        r.lookup("-test")
    with pytest.raises(dg.InvalidGroupName):
        r.resolve("test ")
