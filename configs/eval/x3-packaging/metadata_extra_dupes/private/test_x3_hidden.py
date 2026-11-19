import pytest

from packaging import metadata
from packaging.metadata import ExceptionGroup, InvalidMetadata, Metadata

BASE = {"metadata_version": "2.1", "name": "demo", "version": "1.0"}


def raw(**kw):
    return {**BASE, **kw}


def fields(exc_group):
    return [e.field for e in exc_group.exceptions if isinstance(e, InvalidMetadata)]


@pytest.mark.parametrize("extras", [["Foo", "foo"], ["foo-bar", "foo_bar"], ["a", "b", "A"], ["x.y", "X-Y"]])
def test_duplicate_provides_extra(extras):
    with pytest.raises(ExceptionGroup) as ei:
        Metadata.from_raw(raw(provides_extra=extras))
    assert "provides-extra" in fields(ei.value)


def test_duplicate_provides_extra_without_validate():
    meta = Metadata.from_raw({"provides_extra": ["Foo", "foo"]}, validate=False)
    with pytest.raises(InvalidMetadata) as ei:
        meta.provides_extra
    assert ei.value.field == "provides-extra"


def test_distinct_provides_extra():
    meta = Metadata.from_raw(raw(provides_extra=["Test_Utils", "docs"]))
    assert meta.provides_extra == ["test-utils", "docs"]


@pytest.mark.parametrize(
    "req",
    [
        'pytest; extra == "docs"',
        'pytest; "docs" == extra',
        'pytest; python_version >= "3.8" and (extra == "test" or extra == "docs")',
        'pytest; extra != "docs"',
    ],
)
def test_undeclared_extra(req):
    with pytest.raises(ExceptionGroup) as ei:
        Metadata.from_raw(raw(provides_extra=["test"], requires_dist=[req]))
    assert "requires-dist" in fields(ei.value)


@pytest.mark.parametrize(
    "req",
    [
        'pytest; extra == "test"',
        'pytest; extra == "Test_Utils"',
        'pytest; python_version >= "3.8" and (extra == "test" or extra == "test-utils")',
        'pytest; os_name == "nt"',
        "pytest",
        'pytest; "docs" in extras',
    ],
)
def test_declared_or_unchecked(req):
    meta = Metadata.from_raw(raw(provides_extra=["test", "test.utils"], requires_dist=[req]))
    assert [str(r) for r in meta.requires_dist] == [str(metadata.requirements.Requirement(req))]


def test_no_provides_extra_field_skips_check():
    meta = Metadata.from_raw(raw(requires_dist=['pytest; extra == "docs"']))
    assert meta.provides_extra is None


def test_validate_false_skips_check():
    meta = Metadata.from_raw(raw(provides_extra=["test"], requires_dist=['pytest; extra == "docs"']), validate=False)
    assert len(meta.requires_dist) == 1


def test_from_email():
    text = "Metadata-Version: 2.1\nName: demo\nVersion: 1.0\nProvides-Extra: test\nRequires-Dist: pytest; extra == 'docs'\n"
    with pytest.raises(ExceptionGroup) as ei:
        Metadata.from_email(text)
    assert "requires-dist" in fields(ei.value)


def test_from_email_ok():
    text = "Metadata-Version: 2.1\nName: demo\nVersion: 1.0\nProvides-Extra: test\nRequires-Dist: pytest; extra == 'test'\n"
    assert Metadata.from_email(text).provides_extra == ["test"]
