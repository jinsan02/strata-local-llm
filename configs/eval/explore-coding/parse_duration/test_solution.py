import pytest

from solution import parse_duration


@pytest.mark.parametrize("s,v", [("1h30m", 5400), ("2d", 172800), ("45s", 45), ("1d2h3m4s", 93784),
                                 ("  10m ", 600), ("0s", 0)])
def test_valid(s, v):
    assert parse_duration(s) == v


@pytest.mark.parametrize("s", ["", "   ", "10", "1m1h", "1h1h", "5x", "1 h", "h", "-1s", "1.5h"])
def test_invalid(s):
    with pytest.raises(ValueError):
        parse_duration(s)
