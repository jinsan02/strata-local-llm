"""Y4 채점 테스트 (비공개): 새 함수의 동작 + 두 호출부가 그것을 쓰는지(구조) + 겉 동작 유지."""
import ast
import inspect
import textwrap

import pytest

import packaging.utils as U
from packaging.version import InvalidVersion, Version


def _fn_ast(fn):
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


def _calls(tree, name):
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call) and (
        (isinstance(n.func, ast.Name) and n.func.id == name) or (isinstance(n.func, ast.Attribute) and n.func.attr == name))]


def test_helper_exists_and_signature():
    f = U._parse_filename_version
    sig = inspect.signature(f)
    params = list(sig.parameters.values())
    assert [p.name for p in params[:2]] == ["version_part", "filename"]
    assert sig.parameters["error"].kind is inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["kind"].kind is inspect.Parameter.KEYWORD_ONLY


def test_helper_returns_version():
    v = U._parse_filename_version("1.2.3", "x", error=U.InvalidWheelFilename, kind="wheel")
    assert isinstance(v, Version) and v == Version("1.2.3")


@pytest.mark.parametrize(("error", "kind"), [(U.InvalidWheelFilename, "wheel"), (U.InvalidSdistFilename, "sdist"), (ValueError, "thing")])
def test_helper_raises(error, kind):
    with pytest.raises(error) as ei:
        U._parse_filename_version("not.a.version!", "file-name", error=error, kind=kind)
    assert str(ei.value) == f"Invalid {kind} filename (invalid version): 'file-name'"
    assert isinstance(ei.value.__cause__, InvalidVersion)


@pytest.mark.parametrize("fn", ["parse_wheel_filename", "parse_sdist_filename"])
def test_callers_use_helper(fn):
    tree = _fn_ast(getattr(U, fn))
    assert _calls(tree, "_parse_filename_version"), f"{fn} 가 _parse_filename_version 을 부르지 않는다"
    assert not _calls(tree, "Version"), f"{fn} 안에 Version(...) 직접 호출이 남아 있다"
    for h in (n for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler)):
        names = {x.id for x in ast.walk(h.type) if isinstance(x, ast.Name)} if h.type is not None else set()
        assert "InvalidVersion" not in names, f"{fn} 안에 except InvalidVersion 이 남아 있다"


def test_wheel_behaviour_unchanged():
    assert U.parse_wheel_filename("foo-1.0-py3-none-any.whl")[1] == Version("1.0")
    with pytest.raises(U.InvalidWheelFilename) as ei:
        U.parse_wheel_filename("foo-1.0.x!y-py3-none-any.whl")
    assert str(ei.value) == "Invalid wheel filename (invalid version): 'foo-1.0.x!y-py3-none-any'"
    assert isinstance(ei.value.__cause__, InvalidVersion)


def test_sdist_behaviour_unchanged():
    assert U.parse_sdist_filename("foo-1.0.tar.gz") == ("foo", Version("1.0"))
    with pytest.raises(U.InvalidSdistFilename) as ei:
        U.parse_sdist_filename("foo-1.0.x!y.zip")
    assert str(ei.value) == "Invalid sdist filename (invalid version): 'foo-1.0.x!y.zip'"
    assert isinstance(ei.value.__cause__, InvalidVersion)


def test_all_unchanged():
    assert "_parse_filename_version" not in U.__all__
