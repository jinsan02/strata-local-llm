import pytest

from packaging.tags import Tag
from packaging.utils import InvalidWheelFilename, parse_wheel_filename

LINUX = "foo-1.0-cp312-cp312-manylinux_2_17_x86_64.whl"
WIN = "foo-1.0-py3-none-win32.win_amd64.whl"
PURE = "foo-1.0-py3-none-any.whl"


def test_none_is_unchanged():
    assert parse_wheel_filename(LINUX, platforms=None) == parse_wheel_filename(LINUX)


@pytest.mark.parametrize(
    ("filename", "platforms"),
    [
        (LINUX, ["manylinux_2_17_x86_64"]),
        (LINUX, ["manylinux-2.17-x86_64"]),
        (LINUX, ("win_amd64", "MANYLINUX_2_17_X86_64")),
        (WIN, ["win_amd64"]),
        (WIN, {"win32"}),
        (WIN, ["Win-AMD64"]),
        ("foo-1.0-cp312-cp312-macosx_11_0_arm64.whl", ["macosx-11.0-arm64"]),
        ("foo-1.0-py3-none-my_platform.whl", ["my platform"]),
        (PURE, ["win_amd64"]),
        (PURE, []),
    ],
)
def test_matching_platforms(filename, platforms):
    assert parse_wheel_filename(filename, platforms=platforms) == parse_wheel_filename(filename)


def test_generator_is_accepted():
    out = parse_wheel_filename(WIN, platforms=(p for p in ["linux_x86_64", "win_amd64"]))
    assert out[3] == {Tag("py3", "none", "win32"), Tag("py3", "none", "win_amd64")}


@pytest.mark.parametrize(
    ("filename", "platforms"),
    [
        (LINUX, ["win_amd64"]),
        (LINUX, ["manylinux_2_17"]),
        (WIN, ["linux_x86_64", "macosx_11_0_arm64"]),
        (WIN, []),
    ],
)
def test_no_matching_platform(filename, platforms):
    with pytest.raises(InvalidWheelFilename):
        parse_wheel_filename(filename, platforms=platforms)


def test_str_is_rejected():
    with pytest.raises(TypeError):
        parse_wheel_filename(WIN, platforms="win_amd64")


def test_filename_errors_first():
    with pytest.raises(InvalidWheelFilename, match="extension"):
        parse_wheel_filename("foo-1.0-py3-none-any.zip", platforms=["any"])
    with pytest.raises(InvalidWheelFilename, match="version"):
        parse_wheel_filename("foo-notaversion-py3-none-win_amd64.whl", platforms=["linux_x86_64"])


def test_with_validate_order():
    assert parse_wheel_filename(WIN, validate_order=True, platforms=["win32"])[0] == "foo"
    with pytest.raises(InvalidWheelFilename):
        parse_wheel_filename("foo-1.0-py3-none-win_amd64.win32.whl", validate_order=True, platforms=["win32"])
