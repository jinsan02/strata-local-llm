### EDIT: tests/test_y_canonicalize_version.py
<<<<<<< SEARCH
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

"""
Tests for canonicalize_version that pin its current behaviour.

If someone changes canonicalize_version (or the _trim_release helper it relies on),
these tests should fail, alerting the reviewer.
"""

from __future__ import annotations

import pytest
from packaging.utils import canonicalize_version
from packaging.version import InvalidVersion, Version


# ── Basic string input ──────────────────────────────────────────────────────

class TestBasicStringInput:
    """canonicalize_version('1.0.1') → '1.0.1' (doctest example)."""

    def test_simple_version(self) -> None:
        assert canonicalize_version("1.0.1") == "1.0.1"

    def test_two_part(self) -> None:
        assert canonicalize_version("1.0") == "1"

    def test_single_part(self) -> None:
        assert canonicalize_version("1") == "1"

    def test_three_part_no_trailing_zero(self) -> None:
        assert canonicalize_version("1.2.3") == "1.2.3"


# ── strip_trailing_zero=True (default) ──────────────────────────────────────

class TestStripTrailingZeroDefault:
    """With strip_trailing_zero=True (the default), trailing zeros in the
    release segment are removed, but at least one component is kept."""

    def test_1_0_0(self) -> None:
        assert canonicalize_version("1.0.0") == "1"

    def test_1_4_0_0_0(self) -> None:
        assert canonicalize_version("1.4.0.0.0") == "1.4"

    def test_1_40_0(self) -> None:
        assert canonicalize_version("1.40.0") == "1.40"

    def test_0_0(self) -> None:
        assert canonicalize_version("0.0") == "0"

    def test_0_0_0_0(self) -> None:
        assert canonicalize_version("0.0.0.0") == "0"

    def test_100_0(self) -> None:
        assert canonicalize_version("100.0") == "100"


# ── strip_trailing_zero=False ──────────────────────────────────────────────

class TestStripTrailingZeroFalse:
    """With strip_trailing_zero=False the full release segment is kept."""

    def test_1_4_0(self) -> None:
        assert canonicalize_version("1.4.0", strip_trailing_zero=False) == "1.4.0"

    def test_1_0(self) -> None:
        assert canonicalize_version("1.0", strip_trailing_zero=False) == "1.0"

    def test_1_4_0_0_0(self) -> None:
        assert canonicalize_version("1.4.0.0.0", strip_trailing_zero=False) == "1.4.0.0.0"

    def test_0_0(self) -> None:
        assert canonicalize_version("0.0", strip_trailing_zero=False) == "0.0"


# ── Invalid version strings ────────────────────────────────────────────────

class TestInvalidVersionStrings:
    """Invalid versions are returned unaltered (doctest example: 'foo bar baz')."""

    def test_foo_bar_baz(self) -> None:
        assert canonicalize_version("foo bar baz") == "foo bar baz"

    def test_lolwat(self) -> None:
        assert canonicalize_version("lolwat") == "lolwat"

    def test_1_0_1_test7(self) -> None:
        assert canonicalize_version("1.0.1-test7") == "1.0.1-test7"

    def test_empty_string(self) -> None:
        assert canonicalize_version("") == ""

    def test_random_gibberish(self) -> None:
        assert canonicalize_version("!!!") == "!!!"

    def test_invalid_with_strip_false(self) -> None:
        assert canonicalize_version("lolwat", strip_trailing_zero=False) == "lolwat"


# ── Version object input ───────────────────────────────────────────────────

class TestVersionObjectInput:
    """When a Version instance is passed, it is used directly (no re-parse)."""

    def test_version_object_default(self) -> None:
        v = Version("1.4.0")
        assert canonicalize_version(v) == "1.4"

    def test_version_object_strip_false(self) -> None:
        v = Version("1.4.0")
        assert canonicalize_version(v, strip_trailing_zero=False) == "1.4.0"

    def test_version_object_1_0_0(self) -> None:
        v = Version("1.0.0")
        assert canonicalize_version(v) == "1"

    def test_version_object_0_0(self) -> None:
        v = Version("0.0")
        assert canonicalize_version(v) == "0"

    def test_version_object_1_0_1(self) -> None:
        v = Version("1.0.1")
        assert canonicalize_version(v) == "1.0.1"


# ── Epoch handling ─────────────────────────────────────────────────────────

class TestEpoch:
    """Epochs are preserved in canonical form."""

    def test_epoch_100(self) -> None:
        assert canonicalize_version("100!0.0") == "100!0"

    def test_epoch_100_strip_false(self) -> None:
        assert canonicalize_version("100!0.0", strip_trailing_zero=False) == "100!0.0"

    def test_epoch_1(self) -> None:
        assert canonicalize_version("1!1.0.0") == "1!1"

    def test_epoch_0_default(self) -> None:
        """Epoch 0 is omitted in the string representation."""
        assert canonicalize_version("0!1.0.0") == "1"


# ── Pre-release segments ───────────────────────────────────────────────────

class TestPreRelease:
    """Pre-release parts are kept as-is (they are not part of the release
    segment that gets trimmed)."""

    def test_alpha(self) -> None:
        assert canonicalize_version("1.0a0") == "1a0"

    def test_alpha_strip_false(self) -> None:
        assert canonicalize_version("1.0a0", strip_trailing_zero=False) == "1.0a0"

    def test_beta(self) -> None:
        assert canonicalize_version("1.0b1") == "1b1"

    def test_rc(self) -> None:
        assert canonicalize_version("1.0rc0") == "1rc0"

    def test_rc_with_release_zeros(self) -> None:
        assert canonicalize_version("1.0.0rc0") == "1rc0"

    def test_pre_with_release_no_trailing_zero(self) -> None:
        assert canonicalize_version("1.2.3a1") == "1.2.3a1"


# ── Post-release segments ──────────────────────────────────────────────────

class TestPostRelease:
    """Post-release parts are kept."""

    def test_post0(self) -> None:
        assert canonicalize_version("1.0.post0") == "1.post0"

    def test_post0_strip_false(self) -> None:
        assert canonicalize_version("1.0.post0", strip_trailing_zero=False) == "1.0.post0"

    def test_post1(self) -> None:
        assert canonicalize_version("1.0.0.post1") == "1.post1"


# ── Development segments ───────────────────────────────────────────────────

class TestDevRelease:
    """Development release parts are kept."""

    def test_dev0(self) -> None:
        assert canonicalize_version("1.0.dev0") == "1.dev0"

    def test_dev0_strip_false(self) -> None:
        assert canonicalize_version("1.0.dev0", strip_trailing_zero=False) == "1.0.dev0"

    def test_dev1(self) -> None:
        assert canonicalize_version("1.0.0.dev1") == "1.dev1"


# ── Local version segments ─────────────────────────────────────────────────

class TestLocalVersion:
    """Local version (+…) parts are kept."""

    def test_local_abc(self) -> None:
        assert canonicalize_version("1.0+abc") == "1+abc"

    def test_local_abc_strip_false(self) -> None:
        assert canonicalize_version("1.0+abc", strip_trailing_zero=False) == "1.0+abc"

    def test_local_complex(self) -> None:
        assert canonicalize_version("1.0+local.123") == "1+local.123"


# ── Combined segments ──────────────────────────────────────────────────────

class TestCombinedSegments:
    """Versions with multiple segments (epoch, pre, post, dev, local) work
    together correctly."""

    def test_epoch_pre_post_dev_local(self) -> None:
        """A version with every segment type."""
        assert canonicalize_version("1!2.0.0a1.post3.dev5+local.1") == "1!2a1.post3.dev5+local.1"

    def test_pre_post(self) -> None:
        assert canonicalize_version("1.0a1.post1") == "1a1.post1"

    def test_post_dev(self) -> None:
        assert canonicalize_version("1.0.post1.dev1") == "1.post1.dev1"


# ── Round-trip / consistency ───────────────────────────────────────────────

class TestRoundTrip:
    """Passing a Version object and passing its string should give the same
    result (when the string is valid)."""

    def test_roundtrip_string_vs_object(self) -> None:
        s = "1.4.0.0"
        v = Version(s)
        assert canonicalize_version(v) == canonicalize_version(s)

    def test_roundtrip_with_strip_false(self) -> None:
        s = "1.4.0.0"
        v = Version(s)
        assert canonicalize_version(v, strip_trailing_zero=False) == canonicalize_version(
            s, strip_trailing_zero=False
        )

    def test_roundtrip_invalid(self) -> None:
        """For invalid strings, there is no Version object, so this test
        only checks the string path."""
        assert canonicalize_version("not a version") == "not a version"


# ── Edge cases ─────────────────────────────────────────────────────────────

class TestEdgeCases:
    """Various edge cases."""

    def test_release_all_zeros(self) -> None:
        """0.0.0.0.0 → 0."""
        assert canonicalize_version("0.0.0.0.0") == "0"

    def test_release_all_zeros_strip_false(self) -> None:
        assert canonicalize_version("0.0.0.0.0", strip_trailing_zero=False) == "0.0.0.0.0"

    def test_large_release_numbers(self) -> None:
        assert canonicalize_version("1.2.3.4.5.0") == "1.2.3.4.5"

    def test_no_release_zeros(self) -> None:
        """When there are no trailing zeros, the version is unchanged."""
        assert canonicalize_version("1.2.3") == "1.2.3"

    def test_single_digit(self) -> None:
        assert canonicalize_version("42") == "42"

    def test_single_digit_strip_false(self) -> None:
        assert canonicalize_version("42", strip_trailing_zero=False) == "42"
=======
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

"""
Tests for canonicalize_version that pin its current behaviour.

If someone changes canonicalize_version (or the _trim_release helper it relies on),
these tests should fail, alerting the reviewer.
"""

from __future__ import annotations

import pytest
from packaging.utils import canonicalize_version
from packaging.version import InvalidVersion, Version


# ── Basic string input ──────────────────────────────────────────────────────

class TestBasicStringInput:
    """canonicalize_version('1.0.1') → '1.0.1' (doctest example)."""

    def test_simple_version(self) -> None:
        assert canonicalize_version("1.0.1") == "1.0.1"

    def test_two_part(self) -> None:
        assert canonicalize_version("1.0") == "1"

    def test_single_part(self) -> None:
        assert canonicalize_version("1") == "1"

    def test_three_part_no_trailing_zero(self) -> None:
        assert canonicalize_version("1.2.3") == "1.2.3"


# ── strip_trailing_zero=True (default) ──────────────────────────────────────

class TestStripTrailingZeroDefault:
    """With strip_trailing_zero=True (the default), trailing zeros in the
    release segment are removed, but at least one component is kept."""

    def test_1_0_0(self) -> None:
        assert canonicalize_version("1.0.0") == "1"

    def test_1_4_0_0_0(self) -> None:
        assert canonicalize_version("1.4.0.0.0") == "1.4"

    def test_1_40_0(self) -> None:
        assert canonicalize_version("1.40.0") == "1.40"

    def test_0_0(self) -> None:
        assert canonicalize_version("0.0") == "0"

    def test_0_0_0_0(self) -> None:
        assert canonicalize_version("0.0.0.0") == "0"

    def test_100_0(self) -> None:
        assert canonicalize_version("100.0") == "100"


# ── strip_trailing_zero=False ──────────────────────────────────────────────

class TestStripTrailingZeroFalse:
    """With strip_trailing_zero=False the full release segment is kept."""

    def test_1_4_0(self) -> None:
        assert canonicalize_version("1.4.0", strip_trailing_zero=False) == "1.4.0"

    def test_1_0(self) -> None:
        assert canonicalize_version("1.0", strip_trailing_zero=False) == "1.0"

    def test_1_4_0_0_0(self) -> None:
        assert canonicalize_version("1.4.0.0.0", strip_trailing_zero=False) == "1.4.0.0.0"

    def test_0_0(self) -> None:
        assert canonicalize_version("0.0", strip_trailing_zero=False) == "0.0"


# ── Invalid version strings ────────────────────────────────────────────────

class TestInvalidVersionStrings:
    """Invalid versions are returned unaltered (doctest example: 'foo bar baz')."""

    def test_foo_bar_baz(self) -> None:
        assert canonicalize_version("foo bar baz") == "foo bar baz"

    def test_lolwat(self) -> None:
        assert canonicalize_version("lolwat") == "lolwat"

    def test_1_0_1_test7(self) -> None:
        assert canonicalize_version("1.0.1-test7") == "1.0.1-test7"

    def test_empty_string(self) -> None:
        assert canonicalize_version("") == ""

    def test_random_gibberish(self) -> None:
        assert canonicalize_version("!!!") == "!!!"

    def test_invalid_with_strip_false(self) -> None:
        assert canonicalize_version("lolwat", strip_trailing_zero=False) == "lolwat"


# ── Version object input ───────────────────────────────────────────────────

class TestVersionObjectInput:
    """When a Version instance is passed, it is used directly (no re-parse)."""

    def test_version_object_default(self) -> None:
        v = Version("1.4.0")
        assert canonicalize_version(v) == "1.4"

    def test_version_object_strip_false(self) -> None:
        v = Version("1.4.0")
        assert canonicalize_version(v, strip_trailing_zero=False) == "1.4.0"

    def test_version_object_1_0_0(self) -> None:
        v = Version("1.0.0")
        assert canonicalize_version(v) == "1"

    def test_version_object_0_0(self) -> None:
        v = Version("0.0")
        assert canonicalize_version(v) == "0"

    def test_version_object_1_0_1(self) -> None:
        v = Version("1.0.1")
        assert canonicalize_version(v) == "1.0.1"


# ── Epoch handling ─────────────────────────────────────────────────────────

class TestEpoch:
    """Epochs are preserved in canonical form."""

    def test_epoch_100(self) -> None:
        assert canonicalize_version("100!0.0") == "100!0"

    def test_epoch_100_strip_false(self) -> None:
        assert canonicalize_version("100!0.0", strip_trailing_zero=False) == "100!0.0"

    def test_epoch_1(self) -> None:
        assert canonicalize_version("1!1.0.0") == "1!1"

    def test_epoch_0_default(self) -> None:
        """Epoch 0 is omitted in the string representation."""
        assert canonicalize_version("0!1.0.0") == "1"


# ── Pre-release segments ───────────────────────────────────────────────────

class TestPreRelease:
    """Pre-release parts are kept as-is (they are not part of the release
    segment that gets trimmed)."""

    def test_alpha(self) -> None:
        assert canonicalize_version("1.0a0") == "1a0"

    def test_alpha_strip_false(self) -> None:
        assert canonicalize_version("1.0a0", strip_trailing_zero=False) == "1.0a0"

    def test_beta(self) -> None:
        assert canonicalize_version("1.0b1") == "1b1"

    def test_rc(self) -> None:
        assert canonicalize_version("1.0rc0") == "1rc0"

    def test_rc_with_release_zeros(self) -> None:
        assert canonicalize_version("1.0.0rc0") == "1rc0"

    def test_pre_with_release_no_trailing_zero(self) -> None:
        assert canonicalize_version("1.2.3a1") == "1.2.3a1"


# ── Post-release segments ──────────────────────────────────────────────────

class TestPostRelease:
    """Post-release parts are kept."""

    def test_post0(self) -> None:
        assert canonicalize_version("1.0.post0") == "1.post0"

    def test_post0_strip_false(self) -> None:
        assert canonicalize_version("1.0.post0", strip_trailing_zero=False) == "1