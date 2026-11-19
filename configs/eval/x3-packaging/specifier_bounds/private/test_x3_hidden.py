import pytest

from packaging.specifiers import SpecifierSet
from packaging.version import Version


def b(spec):
    return SpecifierSet(spec).bounds()


def V(s):
    return Version(s)


def check(spec, lower, upper):
    lo, hi = b(spec)
    for got, want in ((lo, lower), (hi, upper)):
        if want is None:
            assert got is None
        else:
            assert isinstance(got, tuple) and len(got) == 2
            assert isinstance(got[0], Version)
            assert got[0] == V(want[0]) and got[1] is want[1]


@pytest.mark.parametrize(
    ("spec", "lower", "upper"),
    [
        (">=1.0", ("1.0", True), None),
        (">1.0", ("1.0", False), None),
        ("<=2.0", None, ("2.0", True)),
        ("<2.0", None, ("2.0", False)),
        ("==1.5", ("1.5", True), ("1.5", True)),
        ("==1.0+abc", ("1.0+abc", True), ("1.0+abc", True)),
        ("!=1.5", None, None),
        ("", None, None),
    ],
)
def test_single(spec, lower, upper):
    check(spec, lower, upper)


@pytest.mark.parametrize(
    ("spec", "lower", "upper"),
    [
        ("==1.2.*", ("1.2", True), ("1.3", False)),
        ("==1.2.3.*", ("1.2.3", True), ("1.2.4", False)),
        ("==1!2.*", ("1!2", True), ("1!3", False)),
        ("~=1.4.5", ("1.4.5", True), ("1.5", False)),
        ("~=2.2", ("2.2", True), ("3", False)),
        ("~=1.4.5rc1", ("1.4.5rc1", True), ("1.5", False)),
        ("~=1!1.4.5", ("1!1.4.5", True), ("1!1.5", False)),
        ("~=2.2.post3", ("2.2.post3", True), ("3", False)),
    ],
)
def test_wildcard_and_compatible(spec, lower, upper):
    check(spec, lower, upper)


def test_derived_upper_has_no_suffix():
    _, hi = b("~=1.4.5rc1")
    assert str(hi[0]) == "1.5"
    _, hi = b("==1!2.*")
    assert str(hi[0]) == "1!3"


@pytest.mark.parametrize(
    ("spec", "lower", "upper"),
    [
        (">=1.0,<2.0", ("1.0", True), ("2.0", False)),
        (">=1.0,>=1.5,<3,<=2.5", ("1.5", True), ("2.5", True)),
        (">=1.0,>1.0", ("1.0", False), None),
        ("<2,<=2.0", None, ("2", False)),
        ("<=2,<=2.0", None, ("2", True)),
        (">=1.0,!=1.5,<2", ("1.0", True), ("2", False)),
        ("~=1.4.5,!=1.4.7,<1.4.9", ("1.4.5", True), ("1.4.9", False)),
        (">=1.4,==1.4.*", ("1.4", True), ("1.5", False)),
        (">2,<1", ("2", False), ("1", False)),
        ("==1.5,>=1.0", ("1.5", True), ("1.5", True)),
    ],
)
def test_combined(spec, lower, upper):
    check(spec, lower, upper)


def test_prereleases_ignored():
    assert SpecifierSet(">=1.0,<2", prereleases=True).bounds() == SpecifierSet(">=1.0,<2").bounds()


@pytest.mark.parametrize("spec", ["===foobar", ">=1.0,===1.0"])
def test_arbitrary_rejected(spec):
    with pytest.raises(ValueError):
        b(spec)
