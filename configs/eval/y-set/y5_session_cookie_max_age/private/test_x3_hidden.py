"""Y5 채점 테스트 (비공개): SESSION_COOKIE_MAX_AGE 설정 · get_cookie_max_age · 쿠키 속성."""
from datetime import timedelta

import pytest

import flask
from flask.sessions import SecureCookieSessionInterface, SessionInterface


def _app(max_age="unset", permanent=False):
    app = flask.Flask(__name__)
    app.secret_key = "y5-secret"
    app.testing = True
    if max_age != "unset":
        app.config["SESSION_COOKIE_MAX_AGE"] = max_age

    @app.route("/set")
    def set_():
        flask.session["a"] = 1
        flask.session.permanent = permanent
        return "ok"

    @app.route("/clear")
    def clear():
        flask.session.clear()
        return "ok"

    return app


def _session_cookie(rv):
    cookies = [c for c in rv.headers.getlist("Set-Cookie") if c.startswith("session=")]
    assert len(cookies) == 1, rv.headers.getlist("Set-Cookie")
    return cookies[0]


def test_default_config():
    assert "SESSION_COOKIE_MAX_AGE" in flask.Flask.default_config
    assert flask.Flask.default_config["SESSION_COOKIE_MAX_AGE"] is None
    assert flask.Flask(__name__).config["SESSION_COOKIE_MAX_AGE"] is None


def test_default_no_max_age():
    rv = _app().test_client().get("/set")
    assert "Max-Age" not in _session_cookie(rv)


@pytest.mark.parametrize(("value", "seconds"), [(3600, 3600), (0, 0), (timedelta(hours=2), 7200), (timedelta(minutes=1, seconds=30), 90)])
def test_cookie_has_max_age(value, seconds):
    rv = _app(value).test_client().get("/set")
    assert f"Max-Age={seconds}" in _session_cookie(rv)


def test_permanent_has_both():
    rv = _app(600, permanent=True).test_client().get("/set")
    c = _session_cookie(rv)
    assert "Max-Age=600" in c and "Expires=" in c


@pytest.mark.parametrize(("value", "expected"), [(None, None), (5, 5), (timedelta(seconds=42), 42), (timedelta(days=1), 86400)])
def test_get_cookie_max_age_values(value, expected):
    app = _app(value)
    for iface in (SessionInterface(), SecureCookieSessionInterface()):
        got = iface.get_cookie_max_age(app)
        assert got == expected and (got is None or type(got) is int)


@pytest.mark.parametrize("value", [-1, timedelta(seconds=-5)])
def test_negative_is_value_error(value):
    with pytest.raises(ValueError):
        SessionInterface().get_cookie_max_age(_app(value))


@pytest.mark.parametrize("value", ["3600", 1.5, True, False, [1]])
def test_bad_type_is_type_error(value):
    with pytest.raises(TypeError):
        SessionInterface().get_cookie_max_age(_app(value))


def test_custom_interface_override_used():
    class Iface(SecureCookieSessionInterface):
        def get_cookie_max_age(self, app):
            return 123

    app = _app()
    app.session_interface = Iface()
    rv = app.test_client().get("/set")
    assert "Max-Age=123" in _session_cookie(rv)


def test_clear_still_deletes_cookie():
    app = _app(3600)
    client = app.test_client()
    client.get("/set")
    rv = client.get("/clear")
    c = _session_cookie(rv)
    assert "Expires=Thu, 01 Jan 1970" in c or "Max-Age=0" in c
