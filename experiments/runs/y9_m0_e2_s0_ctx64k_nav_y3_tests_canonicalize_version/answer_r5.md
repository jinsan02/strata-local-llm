EDIT: tests/test_y_canonicalize_version.py
<<<<<<< SEARCH
            "abc.def.ghi",
            "1.2.3-beta",  # not a valid pre-release format
            "1..2",
            ".1.2",
            "1.2.",
            "v1.2.3",  # actually valid (leading v is allowed)
            "1.2.3+invalid space",
            "hello",
            "random text with numbers 123",
=======
            "abc.def.ghi",
            "1..2",
            ".1.2",
            "1.2.",
            "1.2.3+invalid space",
            "hello",
            "random text with numbers 123",
>>>>>>> REPLACE