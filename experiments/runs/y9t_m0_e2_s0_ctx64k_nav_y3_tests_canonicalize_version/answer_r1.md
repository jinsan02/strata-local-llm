<tool_call>
<function=edit_file>
<parameter=new_string>
class TestCombinedSegments:
    def test_pre_post_dev(self):
        """A version can have pre, post, and dev — all shown."""
        # 1.0a1.post1.dev1 → release=(1,0) → trim → (1,) → "1a1.post1.dev1"
        assert canonicalize_version("1.0a1.post1.dev1") == "1a1.post1.dev1"

    def test_post_dev(self):
        assert canonicalize_version("1.0.post1.dev1") == "1.post1.dev1"

    def test_pre_dev(self):
        assert canonicalize_version("1.0a1.dev1") == "1a1.dev1"

    def test_all_with_trailing_zeros(self):
        assert canonicalize_version("1.0.0a1.post1.dev1") == "1a1.post1.dev1"

    def test_all_no_strip(self):
        assert canonicalize_version("1.0.0a1.post1.dev1", strip_trailing_zero=False) == "1.0.0a1.post1.dev1"

    def test_epoch_pre_post_dev_local(self):
        # 1!1.0a1.post1.dev1+ubuntu → release=(1,0) → trim → (1,) → "1!1a1.post1.dev1+ubuntu"
        v = "1!1.0a1.post1.dev1+ubuntu"
        assert canonicalize_version(v) == "1!1a1.post1.dev1+ubuntu"

    def test_combined_no_trailing_zeros_preserved(self):
        # 1.0.1a1.post1.dev1 → release=(1,0,1) → no trim → "1.0.1a1.post1.dev1"
        assert canonicalize_version("1.0.1a1.post1.dev1") == "1.0.1a1.post1.dev1"
</parameter>
<parameter=old_string>
class TestCombinedSegments:
    def test_pre_post_dev(self):
        """A version can have pre, post, and dev — all shown."""
        assert canonicalize_version("1.0a1.post1.dev1") == "1.0a1.post1.dev1"

    def test_post_dev(self):
        assert canonicalize_version("1.0.post1.dev1") == "1.0.post1.dev1"

    def test_pre_dev(self):
        assert canonicalize_version("1.0a1.dev1") == "1.0a1.dev1"

    def test_all_with_trailing_zeros(self):
        assert canonicalize_version("1.0.0a1.post1.dev1") == "1.0a1.post1.dev1"

    def test_all_no_strip(self):
        assert canonicalize_version("1.0.0a1.post1.dev1", strip_trailing_zero=False) == "1.0.0a1.post1.dev1"

    def test_epoch_pre_post_dev_local(self):
        v = "1!1.0a1.post1.dev1+ubuntu"
        assert canonicalize_version(v) == "1!1.0a1.post1.dev1+ubuntu"
</parameter>
<parameter=path>
tests/test_y_canonicalize_version.py
</parameter>
</function>
</tool_call>