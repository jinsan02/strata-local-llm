"""Y3 참조 테스트 (비공개, 검증용): 돌연변이를 모두 잡아야 한다."""
import pytest

from packaging.utils import canonicalize_version
from packaging.version import Version


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("1.0.0", "1"),
        ("1.0.1", "1.0.1"),
        ("1.4.0.0.0", "1.4"),
        ("0.0", "0"),
        ("0", "0"),
        ("1!1.0.0", "1!1"),
        ("1.0.0rc1", "1rc1"),
        ("1.0.0.post1", "1.post1"),
        ("1.0.0.dev1", "1.dev1"),
        ("1.0.0+local.1", "1+local.1"),
        ("1.2.0a1.post2.dev3+ubuntu", "1.2a1.post2.dev3+ubuntu"),
        ("01.00.00", "1"),
    ],
)
def test_strip(given, expected):
    assert canonicalize_version(given) == expected


@pytest.mark.parametrize(("given", "expected"), [("1.0.0", "1.0.0"), ("1.0.0rc1", "1.0.0rc1"), ("2!3.0", "2!3.0")])
def test_no_strip(given, expected):
    assert canonicalize_version(given, strip_trailing_zero=False) == expected


@pytest.mark.parametrize("bad", ["foo bar baz", "1.0-", "not a version"])
def test_invalid_returned_unaltered(bad):
    assert canonicalize_version(bad) == bad


def test_version_object():
    assert canonicalize_version(Version("2.0.0")) == "2"
    assert canonicalize_version(Version("2.0.0"), strip_trailing_zero=False) == "2.0.0"
