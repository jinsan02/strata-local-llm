### EDIT: tests/test_y_canonicalize_version.py
<<<<<<< SEARCH
=======
from packaging.utils import canonicalize_version
from packaging.version import Version


# --- 기본 동작: 정상 버전 문자열 ---

def test_canonicalize_version_simple():
    assert canonicalize_version("1.0.1") == "1.0.1"


def test_canonicalize_version_single_digit():
    assert canonicalize_version("1") == "1"


def test_canonicalize_version_two_digits():
    assert canonicalize_version("1.2") == "1.2"


# --- strip_trailing_zero=True (기본값): trailing zero 제거 ---

def test_canonicalize_version_trailing_zeros_stripped():
    assert canonicalize_version("1.0.0") == "1"


def test_canonicalize_version_multiple_trailing_zeros():
    assert canonicalize_version("1.4.0.0.0") == "1.4"


def test_canonicalize_version_all_zeros():
    assert canonicalize_version("0.0.0") == "0"


def test_canonicalize_version_zero_release():
    assert canonicalize_version("0.0") == "0"


def test_canonicalize_version_no_trailing_zeros():
    assert canonicalize_version("1.2.3") == "1.2.3"


def test_canonicalize_version_with_strip_trailing_zero_true():
    assert canonicalize_version("1.0.0", strip_trailing_zero=True) == "1"


# --- strip_trailing_zero=False: trailing zero 유지 ---

def test_canonicalize_version_no_strip_trailing_zeros():
    assert canonicalize_version("1.0.0", strip_trailing_zero=False) == "1.0.0"


def test_canonicalize_version_multiple_trailing_zeros_no_strip():
    assert canonicalize_version("1.4.0.0.0", strip_trailing_zero=False) == "1.4.0.0.0"


def test_canonicalize_version_all_zeros_no_strip():
    assert canonicalize_version("0.0.0", strip_trailing_zero=False) == "0.0.0"


# --- 잘못된 버전 문자열: 원본 그대로 반환 ---

def test_canonicalize_version_invalid_returns_original():
    assert canonicalize_version("foo bar baz") == "foo bar baz"


def test_canonicalize_version_invalid_with_strip_false():
    assert canonicalize_version("foo bar baz", strip_trailing_zero=False) == "foo bar baz"


def test_canonicalize_version_empty_string():
    assert canonicalize_version("") == ""


def test_canonicalize_version_invalid_with_spaces():
    assert canonicalize_version(" 1.0 ") == " 1.0 "


# --- Version 객체 입력 ---

def test_canonicalize_version_version_object():
    v = Version("1.0.1")
    assert canonicalize_version(v) == "1.0.1"


def test_canonicalize_version_version_object_trailing_zeros():
    v = Version("1.0.0")
    assert canonicalize_version(v) == "1"


def test_canonicalize_version_version_object_no_strip():
    v = Version("1.0.0")
    assert canonicalize_version(v, strip_trailing_zero=False) == "1.0.0"


# --- epoch이 있는 버전 ---

def test_canonicalize_version_with_epoch():
    assert canonicalize_version("1!1.0.0") == "1!1"


def test_canonicalize_version_with_epoch_no_strip():
    assert canonicalize_version("1!1.0.0", strip_trailing_zero=False) == "1!1.0.0"


def test_canonicalize_version_epoch_only_zero_release():
    assert canonicalize_version("2!0.0.0") == "2!0"


# --- pre-release가 있는 버전 ---

def test_canonicalize_version_with_pre():
    assert canonicalize_version("1.0.0a1") == "1.0.0a1"


def test_canonicalize_version_with_pre_trailing_zeros():
    assert canonicalize_version("1.0.0.0a1") == "1.0.0a1"


def test_canonicalize_version_with_pre_no_strip():
    assert canonicalize_version("1.0.0.0a1", strip_trailing_zero=False) == "1.0.0.0a1"


def test_canonicalize_version_with_beta():
    assert canonicalize_version("2.0b2") == "2.0b2"


def test_canonicalize_version_with_rc():
    assert canonicalize_version("3.0rc1") == "3.0rc1"


# --- post-release가 있는 버전 ---

def test_canonicalize_version_with_post():
    assert canonicalize_version("1.0.post1") == "1.0.post1"


def test_canonicalize_version_with_post_trailing_zeros():
    assert canonicalize_version("1.0.0.post1") == "1.0.post1"


def test_canonicalize_version_with_post_no_strip():
    assert canonicalize_version("1.0.0.post1", strip_trailing_zero=False) == "1.0.0.post1"


# --- dev-release가 있는 버전 ---

def test_canonicalize_version_with_dev():
    assert canonicalize_version("1.0.dev1") == "1.0.dev1"


def test_canonicalize_version_with_dev_trailing_zeros():
    assert canonicalize_version("1.0.0.dev1") == "1.0.dev1"


def test_canonicalize_version_with_dev_no_strip():
    assert canonicalize_version("1.0.0.dev1", strip_trailing_zero=False) == "1.0.0.dev1"


# --- local version이 있는 버전 ---

def test_canonicalize_version_with_local():
    assert canonicalize_version("1.0+ubuntu") == "1.0+ubuntu"


def test_canonicalize_version_with_local_trailing_zeros():
    assert canonicalize_version("1.0.0+ubuntu") == "1.0+ubuntu"


def test_canonicalize_version_with_local_no_strip():
    assert canonicalize_version("1.0.0+ubuntu", strip_trailing_zero=False) == "1.0.0+ubuntu"


def test_canonicalize_version_with_complex_local():
    assert canonicalize_version("2.0.0+linux.amd64") == "2.0+linux.amd64"


# --- 조합: epoch + pre/post/dev/local ---

def test_canonicalize_version_epoch_pre():
    assert canonicalize_version("1!1.0.0a1") == "1!1.0.0a1"


def test_canonicalize_version_epoch_post():
    assert canonicalize_version("1!1.0.0.post1") == "1!1.0.post1"


def test_canonicalize_version_epoch_dev():
    assert canonicalize_version("1!1.0.0.dev1") == "1!1.0.dev1"


def test_canonicalize_version_epoch_local():
    assert canonicalize_version("1!1.0.0+ubuntu") == "1!1.0+ubuntu"


def test_canonicalize_version_all_parts():
    assert canonicalize_version("2!1.0.0a1.post3.dev5+ubuntu") == "2!1.0.0a1.post3.dev5+ubuntu"


def test_canonicalize_version_all_parts_trailing_zeros():
    assert canonicalize_version("2!1.0.0.0a1.post3.dev5+ubuntu") == "2!1.0.0a1.post3.dev5+ubuntu"


# --- Version 객체 + 다양한 부분 ---

def test_canonicalize_version_from_parts_trailing_zeros():
    v = Version.from_parts(epoch=1, release=(1, 0, 0), pre=("a", 1))
    assert canonicalize_version(v) == "1!1.0.0a1"


def test_canonicalize_version_from_parts_no_strip():
    v = Version.from_parts(epoch=1, release=(1, 0, 0), pre=("a", 1))
    assert canonicalize_version(v, strip_trailing_zero=False) == "1!1.0.0a1"


# --- edge cases ---

def test_canonicalize_version_release_single_zero():
    assert canonicalize_version("0") == "0"


def test_canonicalize_version_release_single_zero_no_strip():
    assert canonicalize_version("0", strip_trailing_zero=False) == "0"


def test_canonicalize_version_release_two_zeros():
    assert canonicalize_version("0.0") == "0"


def test_canonicalize_version_release_two_zeros_no_strip():
    assert canonicalize_version("0.0", strip_trailing_zero=False) == "0.0"


def test_canonicalize_version_release_three_zeros():
    assert canonicalize_version("0.0.0") == "0"


def test_canonicalize_version_release_three_zeros_no_strip():
    assert canonicalize_version("0.0.0", strip_trailing_zero=False) == "0.0.0"
>>>>>>> REPLACE