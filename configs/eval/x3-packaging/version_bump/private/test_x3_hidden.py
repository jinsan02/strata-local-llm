import pytest

from packaging.version import Version


@pytest.mark.parametrize(
    ("version", "part", "expected"),
    [
        ("1.2.3", "major", "2.0.0"),
        ("1.2.3", "minor", "1.3.0"),
        ("1.2.3", "micro", "1.2.4"),
        ("1", "micro", "1.0.1"),
        ("1", "minor", "1.1"),
        ("1.2.3.4", "minor", "1.3.0.0"),
        ("1.2.3.4", "major", "2.0.0.0"),
        ("2!1.2.3rc1.post2.dev3+abc", "micro", "2!1.2.4"),
        ("0.9", "major", "1.0"),
        ("1.0.0+local", "major", "2.0.0"),
    ],
)
def test_bump(version, part, expected):
    out = Version(version).bump(part)
    assert isinstance(out, Version)
    assert str(out) == expected


def test_bump_is_new_and_greater():
    v = Version("1.2.3rc1")
    out = v.bump("micro")
    assert out > v
    assert str(v) == "1.2.3rc1"


@pytest.mark.parametrize("bad", ["patch", "MAJOR", "", "dev"])
def test_bad_part(bad):
    with pytest.raises(ValueError):
        Version("1.0").bump(bad)


def test_epoch_kept():
    assert Version("3!4").bump("major").epoch == 3
