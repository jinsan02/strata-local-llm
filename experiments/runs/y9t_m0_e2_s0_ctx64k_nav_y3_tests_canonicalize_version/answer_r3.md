### EDIT: tests/test_y_canonicalize_version.py
<<<<<<<

=======
from __future__ import annotations

import pytest

from packaging.utils import canonicalize_version
from packaging.version import Version


# ── 기본 동작: 유효한 버전 문자열 ──────────────────────────────

class TestBasicValidStrings:
    def test_simple_release(self) -> None:
        assert canonicalize_version("1.0.1") == "1.0.1"

    def test_two_part_release(self) -> None:
        assert canonicalize_version("1.0") == "1.0"

    def test_one_part_release(self) -> None:
        assert canonicalize_version("1") == "1"

    def test_trailing_zeros_stripped(self) -> None:
        """Trailing zeros in release segment are removed by default."""
        assert canonicalize_version("1.0.0") == "1"

    def test_many_trailing_zeros(self) -> None:
        assert canonicalize_version("1.4.0.0.0") == "1.4"

    def test_zero(self) -> None:
        assert canonicalize_version("0") == "0"

    def test_zero_with_trailing_zeros(self) -> None:
        assert canonicalize_version("0.0.0") == "0"


# ── strip_trailing_zero=False ──────────────────────────────────

class TestStripTrailingZeroFalse:
    def test_trailing_zeros_preserved(self) -> None:
        assert canonicalize_version("1.0.0", strip_trailing_zero=False) == "1.0.0"

    def test_no_trailing_zeros_unchanged(self) -> None:
        assert canonicalize_version("1.0.1", strip_trailing_zero=False) == "1.0.1"

    def test_many_trailing_zeros_preserved(self) -> None:
        assert canonicalize_version("1.4.0.0.0", strip_trailing_zero=False) == "1.4.0.0.0"

    def test_single_zero_preserved(self) -> None:
        assert canonicalize_version("0", strip_trailing_zero=False) == "0"


# ── 잘못된 버전 문자열 ─────────────────────────────────────────

class TestInvalidStrings:
    def test_plain_text(self) -> None:
        """Invalid version strings are returned unchanged."""
        assert canonicalize_version("foo bar baz") == "foo bar baz"

    def test_empty_string(self) -> None:
        assert canonicalize_version("") == ""

    def test_random_gibberish(self) -> None:
        assert canonicalize_version("!!!invalid!!!") == "!!!invalid!!!"

    def test_special_chars(self) -> None:
        assert canonicalize_version("@#$%") == "@#$%"


# ── Version 객체 입력 ──────────────────────────────────────────

class TestVersionObjectInput:
    def test_version_obj_default(self) -> None:
        v = Version("1.0.0")
        assert canonicalize_version(v) == "1"

    def test_version_obj_no_trailing_zeros(self) -> None:
        v = Version("1.0.1")
        assert canonicalize_version(v) == "1.0.1"

    def test_version_obj_strip_false(self) -> None:
        v = Version("1.0.0")
        assert canonicalize_version(v, strip_trailing_zero=False) == "1.0.0"

    def test_version_obj_with_pre(self) -> None:
        v = Version("2.0a1")
        assert canonicalize_version(v) == "2.0a1"

    def test_version_obj_with_post(self) -> None:
        v = Version("2.0.post1")
        assert canonicalize_version(v) == "2.0.post1"

    def test_version_obj_with_dev(self) -> None:
        v = Version("2.0.dev1")
        assert canonicalize_version(v) == "2.0.dev1"

    def test_version_obj_with_local(self) -> None:
        v = Version("1.0+local.1")
        assert canonicalize_version(v) == "1+local.1"

    def test_version_obj_with_epoch(self) -> None:
        v = Version("1!2.0.0")
        assert canonicalize_version(v) == "1!2"

    def test_version_obj_with_epoch_strip_false(self) -> None:
        v = Version("1!2.0.0")
        assert canonicalize_version(v, strip_trailing_zero=False) == "1!2.0.0"


# ── Epoch ──────────────────────────────────────────────────────

class TestEpoch:
    def test_epoch_zero_default(self) -> None:
        # epoch 0 is not shown in output
        assert canonicalize_version("0!1.0.0") == "1"

    def test_epoch_nonzero(self) -> None:
        assert canonicalize_version("1!1.0.0") == "1!1"

    def test_epoch_nonzero_strip_false(self) -> None:
        assert canonicalize_version("1!1.0.0", strip_trailing_zero=False) == "1!1.0.0"

    def test_epoch_with_pre(self) -> None:
        assert canonicalize_version("2!1.0a1") == "2!1.0a1"

    def test_epoch_with_post(self) -> None:
        assert canonicalize_version("3!1.0.post1") == "3!1.0.post1"

    def test_epoch_with_dev(self) -> None:
        assert canonicalize_version("1!1.0.dev1") == "1!1.0.dev1"


# ── Pre-release ────────────────────────────────────────────────

class TestPreRelease:
    def test_alpha(self) -> None:
        assert canonicalize_version("1.0a1") == "1.0a1"

    def test_beta(self) -> None:
        assert canonicalize_version("1.0b1") == "1.0b1"

    def test_rc(self) -> None:
        assert canonicalize_version("1.0rc1") == "1.0rc1"

    def test_long_form_alpha(self) -> None:
        assert canonicalize_version("1.0alpha1") == "1.0a1"

    def test_long_form_beta(self) -> None:
        assert canonicalize_version("1.0beta1") == "1.0b1"

    def test_long_form_preview(self) -> None:
        assert canonicalize_version("1.0preview1") == "1.0rc1"

    def test_pre_with_trailing_zeros_in_release(self) -> None:
        # release has trailing zeros but pre-release keeps the trimmed part
        assert canonicalize_version("1.0.0a1") == "1.0a1"

    def test_pre_with_trailing_zeros_strip_false(self) -> None:
        assert canonicalize_version("1.0.0a1", strip_trailing_zero=False) == "1.0.0a1"


# ── Post-release ───────────────────────────────────────────────

class TestPostRelease:
    def test_post_dot(self) -> None:
        assert canonicalize_version("1.0.post1") == "1.0.post1"

    def test_post_dash(self) -> None:
        assert canonicalize_version("1.0-1") == "1.0.post1"

    def test_post_with_trailing_zeros(self) -> None:
        assert canonicalize_version("1.0.0.post1") == "1.0.post1"

    def test_post_with_trailing_zeros_strip_false(self) -> None:
        assert canonicalize_version("1.0.0.post1", strip_trailing_zero=False) == "1.0.0.post1"

    def test_post_zero(self) -> None:
        assert canonicalize_version("1.0.post0") == "1.0.post0"


# ── Development release ────────────────────────────────────────

class TestDevRelease:
    def test_dev(self) -> None:
        assert canonicalize_version("1.0.dev1") == "1.0.dev1"

    def test_dev_with_trailing_zeros(self) -> None:
        assert canonicalize_version("1.0.0.dev1") == "1.0.dev1"

    def test_dev_with_trailing_zeros_strip_false(self) -> None:
        assert canonicalize_version("1.0.0.dev1", strip_trailing_zero=False) == "1.0.0.dev1"


# ── Local version ──────────────────────────────────────────────

class TestLocalVersion:
    def test_local_simple(self) -> None:
        assert canonicalize_version("1.0+ubuntu") == "1+ubuntu"

    def test_local_complex(self) -> None:
        assert canonicalize_version("1.0.0+local.1.foo") == "1+local.1.foo"

    def test_local_with_trailing_zeros_strip_false(self) -> None:
        assert canonicalize_version("1.0.0+local", strip_trailing_zero=False) == "1.0.0+local"

    def test_local_with_epoch(self) -> None:
        assert canonicalize_version("1!1.0+local") == "1!1+local"


# ── Combined segments ──────────────────────────────────────────

class TestCombinedSegments:
    def test_pre_and_post(self) -> None:
        assert canonicalize_version("1.0a1.post1") == "1.0a1.post1"

    def test_pre_and_dev(self) -> None:
        assert canonicalize_version("1.0a1.dev1") == "1.0a1.dev1"

    def test_post_and_dev(self) -> None:
        assert canonicalize_version("1.0.post1.dev1") == "1.0.post1.dev1"

    def test_all_segments(self) -> None:
        assert canonicalize_version("1.0a1.post1.dev1") == "1.0a1.post1.dev1"

    def test_epoch_pre_post_dev_local(self) -> None:
        assert canonicalize_version("1!1.0a1.post1.dev1+local") == "1!1.0a1.post1.dev1+local"


# ── _trim_release 세부 동작 ────────────────────────────────────

class TestTrimReleaseDetails:
    def test_release_all_zeros(self) -> None:
        """All-zero release should leave one zero."""
        assert canonicalize_version("0.0.0.0") == "0"

    def test_release_no_zeros(self) -> None:
        assert canonicalize_version("1.2.3") == "1.2.3"

    def test_release_middle_zeros(self) -> None:
        assert canonicalize_version("1.0.2") == "1.0.2"

    def test_release_single_nonzero_trailing_zero(self) -> None:
        assert canonicalize_version("1.0") == "1.0"

    def test_release_single_nonzero_trailing_zeros(self) -> None:
        assert canonicalize_version("1.0.0") == "1"

    def test_release_many_with_one_nonzero(self) -> None:
        assert canonicalize_version("5.0.0.0.0") == "5"


# ── Version 객체의 내부 캐시 ───────────────────────────────────

class TestVersionCacheBehavior:
    def test_version_obj_key_cache_preserved(self) -> None:
        """_trim_release copies the _key_cache from the original."""
        v = Version("1.0.0")
        # Force key cache computation
        _ = v._key
        result = canonicalize_version(v)
        assert result == "1"
        # The original version's key cache should still be accessible
        _ = v._key

    def test_version_obj_hash_preserved(self) -> None:
        """_trim_release copies the _hash_cache from the original."""
        v = Version("1.0.0")
        h = hash(v)
        result = canonicalize_version(v)
        assert result == "1"
        assert hash(v) == h
>>>>>>>