"""Y1 채점 테스트 (비공개): 사후 릴리스의 개발판(1.0.post1.dev2 등) 정렬 · 비교와 주변 사례."""
import pytest

from packaging.specifiers import SpecifierSet
from packaging.version import Version

# PEP 440 순서대로 (앞이 작다)
ORDERED = [
    "1.0.dev1",
    "1.0.dev2",
    "1.0a1.dev1",
    "1.0a1",
    "1.0a1.post1.dev1",
    "1.0a1.post1",
    "1.0b1",
    "1.0rc1.dev1",
    "1.0rc1",
    "1.0",
    "1.0+local",
    "1.0.post1.dev1",
    "1.0.post1.dev2",
    "1.0.post1",
    "1.0.post1+local",
    "1.0.post2.dev1",
    "1.0.post2",
    "1.1.dev1",
]


def test_report_sorted():
    got = sorted(["1.0", "1.0a1", "1.0.post1.dev2", "1.0.post1"], key=Version)
    assert got == ["1.0a1", "1.0", "1.0.post1.dev2", "1.0.post1"]


def test_report_specifier_contains():
    assert SpecifierSet(">=1.0", prereleases=True).contains("1.0.post1.dev2")


@pytest.mark.parametrize("i", range(len(ORDERED) - 1))
def test_adjacent_order(i):
    a, b = Version(ORDERED[i]), Version(ORDERED[i + 1])
    assert a < b and b > a and a != b


def test_full_sort_is_stable_order():
    shuffled = list(reversed(ORDERED))
    assert [str(v) for v in sorted(map(Version, shuffled))] == ORDERED


@pytest.mark.parametrize(
    ("spec", "version", "expected"),
    [
        (">=1.0", "1.0.post1.dev2", True),
        (">1.0", "1.0.post1.dev2", False),  # PEP 440: > 는 지정 버전의 사후 릴리스를 받지 않는다
        ("<1.0.post2", "1.0.post1.dev2", True),
        ("<1.0.post1", "1.0.post1.dev2", False),  # PEP 440: <V 는 V 자신의 개발판을 받지 않는다
        ("<1.0", "1.0.post1.dev2", False),
        ("<=1.0", "1.0.post1.dev1", False),
        ("==1.0.post1.dev2", "1.0.post1.dev2", True),
        (">=1.0a1", "1.0.dev1", False),
        ("<1.0a1", "1.0.dev1", True),
    ],
)
def test_specifier_with_prereleases(spec, version, expected):
    assert SpecifierSet(spec, prereleases=True).contains(version) is expected


def test_filter_keeps_postdev():
    got = list(SpecifierSet(">=1.0,<2", prereleases=True).filter(["0.9", "1.0.post1.dev2", "1.0a1", "2.0"]))
    assert got == ["1.0.post1.dev2"]


def test_equal_with_trailing_zero_and_hash():
    a, b = Version("1.0.0.post1.dev2"), Version("1.0.post1.dev2")
    assert a == b and hash(a) == hash(b)
    assert Version("1.0.post1.dev2") > Version("1.0.0")


def test_max_of_list():
    assert str(max(map(Version, ["1.0.post1.dev5", "1.0", "1.0rc2"]))) == "1.0.post1.dev5"
