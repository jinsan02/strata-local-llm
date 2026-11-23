"""Y6 채점 테스트 (비공개): Config.require."""
import pytest

import flask
from flask import Config


def _cfg(**kw):
    c = Config(".")
    c.update(kw)
    return c


def test_returns_values_in_order():
    c = _cfg(A=1, B="x", C=[1])
    got = c.require("C", "A")
    assert got == {"C": [1], "A": 1} and list(got) == ["C", "A"]
    assert type(got) is dict


def test_duplicate_key_once():
    got = _cfg(A=1).require("A", "A")
    assert got == {"A": 1} and len(got) == 1


def test_missing_single():
    with pytest.raises(KeyError) as ei:
        _cfg(A=1).require("A", "B")
    assert ei.value.args[0] == "Missing required config keys: B"


def test_missing_all_sorted():
    with pytest.raises(KeyError) as ei:
        _cfg(M=1).require("Z", "M", "B", "K")
    assert ei.value.args[0] == "Missing required config keys: B, K, Z"


def test_none_counts_as_missing():
    with pytest.raises(KeyError) as ei:
        _cfg(A=None, B=0, C="").require("A", "B", "C")
    assert ei.value.args[0] == "Missing required config keys: A"


def test_allow_none():
    assert _cfg(A=None).require("A", allow_none=True) == {"A": None}
    with pytest.raises(KeyError) as ei:
        _cfg(A=None).require("A", "B", allow_none=True)
    assert ei.value.args[0] == "Missing required config keys: B"


def test_falsy_values_ok():
    assert _cfg(A=0, B=False, C="", D=[]).require("A", "B", "C", "D") == {"A": 0, "B": False, "C": "", "D": []}


def test_no_keys_type_error():
    with pytest.raises(TypeError):
        _cfg(A=1).require()


@pytest.mark.parametrize("bad", [1, None, b"A", ("A",)])
def test_non_str_key_type_error(bad):
    with pytest.raises(TypeError):
        _cfg(A=1).require("A", bad)


def test_does_not_modify():
    c = _cfg(A=1)
    before = dict(c)
    with pytest.raises(KeyError):
        c.require("A", "B")
    c.require("A")
    assert dict(c) == before


def test_on_app_config():
    app = flask.Flask(__name__)
    app.config["SECRET_KEY"] = "s"
    assert app.config.require("SECRET_KEY", "TESTING") == {"SECRET_KEY": "s", "TESTING": False}
    with pytest.raises(KeyError) as ei:
        app.config.require("SERVER_NAME")  # 기본값 None
    assert ei.value.args[0] == "Missing required config keys: SERVER_NAME"
