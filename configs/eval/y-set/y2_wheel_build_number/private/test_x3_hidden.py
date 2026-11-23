"""Y2 채점 테스트 (비공개): wheel 파일 이름의 build 번호(여러 자리 · 접미사) 파싱."""
import pytest

from packaging.utils import InvalidWheelFilename, parse_wheel_filename


@pytest.mark.parametrize(
    ("filename", "build"),
    [
        ("foo-1.0-1-py3-none-any.whl", (1, "")),
        ("foo-1.0-10-py3-none-any.whl", (10, "")),
        ("foo-1.0-1000-py3-none-any.whl", (1000, "")),
        ("foo-1.0-123abc-py3-none-any.whl", (123, "abc")),
        ("foo-1.0-42_x-py3-none-any.whl", (42, "_x")),
        ("foo-1.0-007-py3-none-any.whl", (7, "")),
        ("foo-1.0-2024.1-py3-none-any.whl", (2024, ".1")),
        ("foo-1.0-9a9-py3-none-any.whl", (9, "a9")),
    ],
)
def test_build_number(filename, build):
    assert parse_wheel_filename(filename)[2] == build


def test_no_build():
    assert parse_wheel_filename("foo-1.0-py3-none-any.whl")[2] == ()


@pytest.mark.parametrize("filename", ["foo-1.0-abc-py3-none-any.whl", "foo-1.0-_1-py3-none-any.whl"])
def test_build_must_start_with_digit(filename):
    with pytest.raises(InvalidWheelFilename):
        parse_wheel_filename(filename)


def test_build_sorts_numerically():
    names = ["foo-1.0-9-py3-none-any.whl", "foo-1.0-10-py3-none-any.whl", "foo-1.0-100-py3-none-any.whl"]
    builds = sorted(parse_wheel_filename(n)[2] for n in names)
    assert builds == [(9, ""), (10, ""), (100, "")]
