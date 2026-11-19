"""X3 확인 전용 과제 D · E · F 생성 (11-19). 원본(work/packaging-src)은 건드리지 않고 과제마다 사본에서 고쳐 ref.patch 를 뽑는다.

만드는 것: configs/eval/x3-packaging/<task>/{prompt.md, task.json, private/ref.patch, private/test_x3_hidden.py}.
검증(기준 실패 · 참조 통과 · 회귀)은 GPU 측정이 없을 때 validate_def.py 로 따로 한다. 여기서는 정적 점검만:
패치가 고정 커밋에 깨끗이 붙는지(git apply --check), 고친 파일 · 숨은 테스트가 컴파일되는지.
"""
from __future__ import annotations

import json
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(r"C:\strata-lab\work\packaging-src")
DEV = Path(r"C:\strata-lab\work\x3-dev")
TASKS = Path(r"C:\strata-lab\configs\eval\x3-packaging")
COMMIT = "6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc"


def run(*a, cwd):
    r = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"실패 {a}: {r.stderr[-800:]}")
    return r.stdout


def dev_copy(name: str) -> Path:
    d = DEV / name
    if d.exists():
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(d)], capture_output=True)
    DEV.mkdir(parents=True, exist_ok=True)
    run("git", "clone", "-q", "--no-checkout", str(SRC), str(d), cwd=DEV)
    run("git", "checkout", "-q", "--detach", COMMIT, cwd=d)
    return d


def replace(root: Path, rel: str, old: str, new: str) -> None:
    p = root / rel
    t = p.read_text(encoding="utf-8")
    n = t.count(old)
    if n != 1:
        raise SystemExit(f"{rel}: 기준 문자열이 {n}회 (1회여야 함): {old[:80]!r}")
    p.write_text(t.replace(old, new), encoding="utf-8", newline="\n")


# ════════════════════════════════════════════════════════════════════════════
# D tags_platform_filter (A: 한 파일의 규칙 → 다른 파일 호출부)
# ════════════════════════════════════════════════════════════════════════════
D_PROMPT = """`packaging.utils.parse_wheel_filename` 에 키워드 전용 인자 `platforms` 를 추가하라.

- 기본값은 `None` 이고, `None` 이면 지금과 똑같이 동작한다.
- `platforms` 는 플랫폼 이름 문자열의 iterable 이다(리스트 · 튜플 · 집합 · 제너레이터 모두). 문자열 하나(`str`)를 그대로 주면 `TypeError` 를 던진다.
- 주어진 이름은 `packaging.tags` 가 플랫폼 이름을 정규화하는 규칙과 같게 정규화해서 비교한다: `.` · `-` · 공백을 `_` 로 바꾸고 소문자로. 예: `"macosx-11.0-arm64"` → `macosx_11_0_arm64`, `"WIN_AMD64"` → `win_amd64`.
- 파일 이름의 태그 가운데 하나라도 플랫폼이 정규화한 이름 중 하나와 같으면 통과한다. 플랫폼이 `any` 인 태그는 어떤 `platforms` 에도 통과한다(빈 iterable 포함).
- 통과하지 못하면 `InvalidWheelFilename` 을 던진다.
- 파일 이름 자체의 기존 검사(확장자 · 이름 · 버전 · 빌드 번호 · 태그)가 먼저다. 그 오류는 지금과 같은 메시지로 난다.
- 통과하면 반환값은 지금과 같다(태그 집합을 거르지 않는다). `validate_order` 와 함께 쓸 수 있다.
- 기존 동작은 바뀌면 안 된다.
"""

D_TEST = '''import pytest

from packaging.tags import Tag
from packaging.utils import InvalidWheelFilename, parse_wheel_filename

LINUX = "foo-1.0-cp312-cp312-manylinux_2_17_x86_64.whl"
WIN = "foo-1.0-py3-none-win32.win_amd64.whl"
PURE = "foo-1.0-py3-none-any.whl"


def test_none_is_unchanged():
    assert parse_wheel_filename(LINUX, platforms=None) == parse_wheel_filename(LINUX)


@pytest.mark.parametrize(
    ("filename", "platforms"),
    [
        (LINUX, ["manylinux_2_17_x86_64"]),
        (LINUX, ["manylinux-2.17-x86_64"]),
        (LINUX, ("win_amd64", "MANYLINUX_2_17_X86_64")),
        (WIN, ["win_amd64"]),
        (WIN, {"win32"}),
        (WIN, ["Win-AMD64"]),
        ("foo-1.0-cp312-cp312-macosx_11_0_arm64.whl", ["macosx-11.0-arm64"]),
        ("foo-1.0-py3-none-my_platform.whl", ["my platform"]),
        (PURE, ["win_amd64"]),
        (PURE, []),
    ],
)
def test_matching_platforms(filename, platforms):
    assert parse_wheel_filename(filename, platforms=platforms) == parse_wheel_filename(filename)


def test_generator_is_accepted():
    out = parse_wheel_filename(WIN, platforms=(p for p in ["linux_x86_64", "win_amd64"]))
    assert out[3] == {Tag("py3", "none", "win32"), Tag("py3", "none", "win_amd64")}


@pytest.mark.parametrize(
    ("filename", "platforms"),
    [
        (LINUX, ["win_amd64"]),
        (LINUX, ["manylinux_2_17"]),
        (WIN, ["linux_x86_64", "macosx_11_0_arm64"]),
        (WIN, []),
    ],
)
def test_no_matching_platform(filename, platforms):
    with pytest.raises(InvalidWheelFilename):
        parse_wheel_filename(filename, platforms=platforms)


def test_str_is_rejected():
    with pytest.raises(TypeError):
        parse_wheel_filename(WIN, platforms="win_amd64")


def test_filename_errors_first():
    with pytest.raises(InvalidWheelFilename, match="extension"):
        parse_wheel_filename("foo-1.0-py3-none-any.zip", platforms=["any"])
    with pytest.raises(InvalidWheelFilename, match="version"):
        parse_wheel_filename("foo-notaversion-py3-none-win_amd64.whl", platforms=["linux_x86_64"])


def test_with_validate_order():
    assert parse_wheel_filename(WIN, validate_order=True, platforms=["win32"])[0] == "foo"
    with pytest.raises(InvalidWheelFilename):
        parse_wheel_filename("foo-1.0-py3-none-win_amd64.win32.whl", validate_order=True, platforms=["win32"])
'''


def make_d(root: Path) -> None:
    rel = "src/packaging/utils.py"
    replace(root, rel, "from typing import NewType, cast\n\nfrom .tags import InvalidTag, Tag, UnsortedTagsError, parse_tag\n",
            "from typing import TYPE_CHECKING, NewType, cast\n\n"
            "from .tags import InvalidTag, Tag, UnsortedTagsError, _normalize_string, parse_tag\n")
    replace(root, rel, "from .version import InvalidVersion, Version\n",
            "from .version import InvalidVersion, Version\n\nif TYPE_CHECKING:\n    from collections.abc import Iterable\n")
    replace(root, rel, "    validate_order: bool = False,\n) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:",
            "    validate_order: bool = False,\n    platforms: Iterable[str] | None = None,\n"
            ") -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:")
    replace(root, rel, "    :param bool validate_order: Check whether compressed tag set components\n        are in sorted order.\n",
            "    :param bool validate_order: Check whether compressed tag set components\n        are in sorted order.\n"
            "    :param platforms: If given, at least one tag must have one of these\n"
            "        platforms (normalized like :mod:`packaging.tags` platform names) or\n"
            "        the ``any`` platform.\n")
    replace(root, rel, "    if not filename.endswith(\".whl\"):\n        raise InvalidWheelFilename(\n"
            "            f\"Invalid wheel filename (extension must be '.whl'): {filename!r}\"\n        )\n",
            "    if isinstance(platforms, str):\n"
            "        raise TypeError(\"platforms must be an iterable of platform names, not a str\")\n"
            "    if not filename.endswith(\".whl\"):\n        raise InvalidWheelFilename(\n"
            "            f\"Invalid wheel filename (extension must be '.whl'): {filename!r}\"\n        )\n")
    replace(root, rel, "    return (name, version, build, tags)\n\n\ndef parse_sdist_filename",
            "    if platforms is not None:\n"
            "        wanted = {_normalize_string(p).lower() for p in platforms}\n"
            "        if not any(t.platform == \"any\" or t.platform in wanted for t in tags):\n"
            "            raise InvalidWheelFilename(\n"
            "                f\"Invalid wheel filename (no tag for platforms {sorted(wanted)!r}): \"\n"
            "                f\"{filename!r}\"\n"
            "            )\n"
            "    return (name, version, build, tags)\n\n\ndef parse_sdist_filename")


# ════════════════════════════════════════════════════════════════════════════
# E metadata_extra_dupes (B: 두 모듈 — markers 의 마커 구조를 읽고 metadata 에서 검사)
# ════════════════════════════════════════════════════════════════════════════
E_PROMPT = """`packaging.metadata.Metadata` 의 extra 검사를 두 가지 늘려라.

1. **Provides-Extra 중복**: `provides_extra` 값을 처리할 때, 이름을 지금처럼 `canonicalize_name` 으로 정규화한 뒤 같은 이름이 두 번 이상 나오면 `InvalidMetadata` 를 던진다(필드 이름 `provides-extra`). 예: `["Foo", "foo"]`, `["foo-bar", "foo_bar"]`. 이 검사는 `validate=False` 로 만든 객체에서 `provides_extra` 속성에 접근할 때도 일어난다. 중복이 없으면 지금처럼 정규화된 이름 리스트를 돌려준다.
2. **선언되지 않은 extra**: `Metadata.from_raw(..., validate=True)` (따라서 `from_email` 도) 검증에서, `requires_dist` 의 요구사항 마커가 변수 `extra` 를 값과 비교하는 부분(`extra == "docs"` · `"docs" == extra` 처럼, 연산자와 좌우 순서 무관, `and` · `or` · 괄호 안 포함)의 값을 정규화한 이름이 정규화된 `provides_extra` 에 없으면 `InvalidMetadata` 를 낸다(필드 이름 `requires-dist`). 다른 검증 오류와 함께 `ExceptionGroup` 으로 모인다.
   - `provides_extra` 필드가 아예 없으면(값이 `None`) 이 검사는 하지 않는다. `provides_extra` 나 `requires_dist` 자체가 잘못돼 오류가 난 경우에도 이 검사는 건너뛴다.
   - `"docs" in extras` 같은 `extras` 집합 비교는 이 검사 대상이 아니다.
   - `validate=False` 일 때는 이 검사를 하지 않는다.
3. 기존 동작은 바뀌면 안 된다.

마커의 구조는 `packaging.markers` · `packaging._parser` 에 있다.
"""

E_TEST = '''import pytest

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
    text = "Metadata-Version: 2.1\\nName: demo\\nVersion: 1.0\\nProvides-Extra: test\\nRequires-Dist: pytest; extra == 'docs'\\n"
    with pytest.raises(ExceptionGroup) as ei:
        Metadata.from_email(text)
    assert "requires-dist" in fields(ei.value)


def test_from_email_ok():
    text = "Metadata-Version: 2.1\\nName: demo\\nVersion: 1.0\\nProvides-Extra: test\\nRequires-Dist: pytest; extra == 'test'\\n"
    assert Metadata.from_email(text).provides_extra == ["test"]
'''


def make_e(root: Path) -> None:
    rel = "src/packaging/metadata.py"
    replace(root, rel, "from . import licenses, requirements, specifiers, utils\n",
            "from . import licenses, requirements, specifiers, utils\nfrom ._parser import Value, Variable\n")
    replace(root, rel,
            "        normalized_names = []\n"
            "        try:\n"
            "            for name in value:\n"
            "                normalized_names.append(utils.canonicalize_name(name, validate=True))\n"
            "        except utils.InvalidName as exc:\n"
            "            raise self._invalid_metadata(\n"
            "                f\"{name!r} is invalid for {self.raw_name!r}\", cause=exc\n"
            "            ) from exc\n"
            "        else:\n"
            "            return normalized_names\n",
            "        normalized_names = []\n"
            "        try:\n"
            "            for name in value:\n"
            "                normalized_names.append(utils.canonicalize_name(name, validate=True))\n"
            "        except utils.InvalidName as exc:\n"
            "            raise self._invalid_metadata(\n"
            "                f\"{name!r} is invalid for {self.raw_name!r}\", cause=exc\n"
            "            ) from exc\n"
            "        seen: set[str] = set()\n"
            "        for name, normalized in zip(value, normalized_names):\n"
            "            if normalized in seen:\n"
            "                raise self._invalid_metadata(\n"
            "                    f\"{name!r} duplicates another extra in {self.raw_name!r} \"\n"
            "                    f\"(normalized: {normalized!r})\"\n"
            "                )\n"
            "            seen.add(normalized)\n"
            "        return normalized_names\n")
    replace(root, rel, "            collector.finalize(\"invalid metadata\")\n",
            "            with collector.collect(InvalidMetadata):\n"
            "                ins._check_requires_dist_extras()\n\n"
            "            collector.finalize(\"invalid metadata\")\n")
    replace(root, rel, "        return ins\n\n    @classmethod\n    def from_email(",
            "        return ins\n\n"
            "    def _check_requires_dist_extras(self) -> None:\n"
            "        \"\"\"Every ``extra`` compared in a Requires-Dist marker is a Provides-Extra.\n\n"
            "        Uses only the values already validated (cached); skipped when either field\n"
            "        is absent or failed validation.\n"
            "        \"\"\"\n"
            "        declared = self.__dict__.get(\"provides_extra\")\n"
            "        reqs = self.__dict__.get(\"requires_dist\")\n"
            "        if declared is None or not reqs:\n"
            "            return\n"
            "        known = set(declared)\n"
            "        for req in reqs:\n"
            "            if req.marker is None:\n"
            "                continue\n"
            "            for name in sorted(_marker_extra_values(req.marker._markers)):\n"
            "                if name not in known:\n"
            "                    raise InvalidMetadata(\n"
            "                        \"requires-dist\",\n"
            "                        f\"{str(req)!r} uses extra {name!r} which is not in \"\n"
            "                        f\"'provides-extra'\",\n"
            "                    )\n\n"
            "    @classmethod\n    def from_email(")
    replace(root, rel, "class Metadata:\n",
            "def _marker_extra_values(markers: object) -> set[str]:\n"
            "    \"\"\"Normalized values compared with the ``extra`` variable in a marker tree.\"\"\"\n"
            "    found: set[str] = set()\n"
            "    if isinstance(markers, list):\n"
            "        for item in markers:\n"
            "            found |= _marker_extra_values(item)\n"
            "    elif isinstance(markers, tuple) and len(markers) == 3:\n"
            "        lhs, _op, rhs = markers\n"
            "        if isinstance(lhs, Variable) and lhs.value == \"extra\" and isinstance(rhs, Value):\n"
            "            found.add(utils.canonicalize_name(rhs.value))\n"
            "        elif isinstance(rhs, Variable) and rhs.value == \"extra\" and isinstance(lhs, Value):\n"
            "            found.add(utils.canonicalize_name(lhs.value))\n"
            "    return found\n\n\n"
            "class Metadata:\n")


# ════════════════════════════════════════════════════════════════════════════
# F specifier_bounds (C: 실패 로그 보고 1회 보완)
# ════════════════════════════════════════════════════════════════════════════
F_PROMPT = """`packaging.specifiers.SpecifierSet` 에 메서드 `bounds()` 를 추가하라. 반환값은 `(lower, upper)` 튜플이고, 각각 `None`(제한 없음)이거나 `(Version, inclusive: bool)` 이다.

각 specifier 가 주는 경계 (`V` 는 specifier 의 버전):

| 연산자 | lower | upper |
| --- | --- | --- |
| `>=V` | `(V, True)` | — |
| `>V` | `(V, False)` | — |
| `<=V` | — | `(V, True)` |
| `<V` | — | `(V, False)` |
| `==V` (와일드카드 아님) | `(V, True)` | `(V, True)` |
| `==V.*` | `(V, True)` | release 의 마지막 숫자를 1 올린 버전, `False` |
| `~=V` | `(V, True)` | release 의 마지막 숫자를 버리고, 남은 마지막 숫자를 1 올린 버전, `False` |
| `!=V` | — | — |

- 와일드카드 · `~=` 의 upper 는 epoch 를 유지하고 release 숫자만으로 만든다(pre · post · dev · local 없음). 예: `==1.2.*` → `(1.2, True)`, `(1.3, False)` · `==1!2.*` → upper `1!3` · `~=1.4.5` → upper `1.5` · `~=2.2` → upper `3` · `~=1.4.5rc1` → lower `1.4.5rc1`, upper `1.5`.
- 여러 specifier 의 경계는 합친다: lower 는 가장 큰 것, upper 는 가장 작은 것. 버전이 같으면(`Version` 비교로 같음, 예: `2` 와 `2.0`) `inclusive=False` 쪽이 이긴다.
- 빈 `SpecifierSet` 은 `(None, None)`. 결과가 공집합인지는 따지지 않는다(예: `>2,<1` 도 그대로 반환).
- `===` 가 하나라도 있으면 `ValueError` 를 던진다.
- prerelease 설정은 결과에 영향을 주지 않는다. 기존 동작은 바뀌면 안 된다.
"""

F_TEST = '''import pytest

from packaging.specifiers import SpecifierSet
from packaging.version import Version


def b(spec):
    return SpecifierSet(spec).bounds()


def V(s):
    return Version(s)


def check(spec, lower, upper):
    lo, hi = b(spec)
    for got, want in ((lo, lower), (hi, upper)):
        if want is None:
            assert got is None
        else:
            assert isinstance(got, tuple) and len(got) == 2
            assert isinstance(got[0], Version)
            assert got[0] == V(want[0]) and got[1] is want[1]


@pytest.mark.parametrize(
    ("spec", "lower", "upper"),
    [
        (">=1.0", ("1.0", True), None),
        (">1.0", ("1.0", False), None),
        ("<=2.0", None, ("2.0", True)),
        ("<2.0", None, ("2.0", False)),
        ("==1.5", ("1.5", True), ("1.5", True)),
        ("==1.0+abc", ("1.0+abc", True), ("1.0+abc", True)),
        ("!=1.5", None, None),
        ("", None, None),
    ],
)
def test_single(spec, lower, upper):
    check(spec, lower, upper)


@pytest.mark.parametrize(
    ("spec", "lower", "upper"),
    [
        ("==1.2.*", ("1.2", True), ("1.3", False)),
        ("==1.2.3.*", ("1.2.3", True), ("1.2.4", False)),
        ("==1!2.*", ("1!2", True), ("1!3", False)),
        ("~=1.4.5", ("1.4.5", True), ("1.5", False)),
        ("~=2.2", ("2.2", True), ("3", False)),
        ("~=1.4.5rc1", ("1.4.5rc1", True), ("1.5", False)),
        ("~=1!1.4.5", ("1!1.4.5", True), ("1!1.5", False)),
        ("~=2.2.post3", ("2.2.post3", True), ("3", False)),
    ],
)
def test_wildcard_and_compatible(spec, lower, upper):
    check(spec, lower, upper)


def test_derived_upper_has_no_suffix():
    _, hi = b("~=1.4.5rc1")
    assert str(hi[0]) == "1.5"
    _, hi = b("==1!2.*")
    assert str(hi[0]) == "1!3"


@pytest.mark.parametrize(
    ("spec", "lower", "upper"),
    [
        (">=1.0,<2.0", ("1.0", True), ("2.0", False)),
        (">=1.0,>=1.5,<3,<=2.5", ("1.5", True), ("2.5", True)),
        (">=1.0,>1.0", ("1.0", False), None),
        ("<2,<=2.0", None, ("2", False)),
        ("<=2,<=2.0", None, ("2", True)),
        (">=1.0,!=1.5,<2", ("1.0", True), ("2", False)),
        ("~=1.4.5,!=1.4.7,<1.4.9", ("1.4.5", True), ("1.4.9", False)),
        (">=1.4,==1.4.*", ("1.4", True), ("1.5", False)),
        (">2,<1", ("2", False), ("1", False)),
        ("==1.5,>=1.0", ("1.5", True), ("1.5", True)),
    ],
)
def test_combined(spec, lower, upper):
    check(spec, lower, upper)


def test_prereleases_ignored():
    assert SpecifierSet(">=1.0,<2", prereleases=True).bounds() == SpecifierSet(">=1.0,<2").bounds()


@pytest.mark.parametrize("spec", ["===foobar", ">=1.0,===1.0"])
def test_arbitrary_rejected(spec):
    with pytest.raises(ValueError):
        b(spec)
'''


def make_f(root: Path) -> None:
    rel = "src/packaging/specifiers.py"
    replace(root, rel, "    def __len__(self) -> int:\n        \"\"\"Returns the number of specifiers in this specifier set.\"\"\"\n",
            "    def bounds(\n        self,\n"
            "    ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:\n"
            "        \"\"\"The (lower, upper) bounds of this set, each ``None`` or ``(version, inclusive)``.\n\n"
            "        ``!=`` adds no bound; ``==V.*`` and ``~=V`` give an exclusive upper bound built\n"
            "        from the release numbers (epoch kept). The tightest bound wins; on equal\n"
            "        versions the exclusive one wins. Emptiness is not checked.\n\n"
            "        :raises ValueError: If the set has an ``===`` specifier.\n"
            "        \"\"\"\n\n"
            "        def release_version(epoch: int, release: list[int]) -> Version:\n"
            "            text = \".\".join(str(x) for x in release)\n"
            "            return Version(f\"{epoch}!{text}\" if epoch else text)\n\n"
            "        lower: tuple[Version, bool] | None = None\n"
            "        upper: tuple[Version, bool] | None = None\n"
            "        for spec in self._specs:\n"
            "            op, ver = spec.operator, spec.version\n"
            "            lo: tuple[Version, bool] | None = None\n"
            "            hi: tuple[Version, bool] | None = None\n"
            "            if op == \"===\":\n"
            "                raise ValueError(f\"cannot compute bounds of {str(spec)!r}\")\n"
            "            if op == \"==\" and ver.endswith(\".*\"):\n"
            "                base = Version(ver[:-2])\n"
            "                nxt = list(base.release)\n"
            "                nxt[-1] += 1\n"
            "                lo, hi = (base, True), (release_version(base.epoch, nxt), False)\n"
            "            elif op == \"==\":\n"
            "                lo = hi = (Version(ver), True)\n"
            "            elif op == \"~=\":\n"
            "                base = Version(ver)\n"
            "                nxt = list(base.release[:-1])\n"
            "                nxt[-1] += 1\n"
            "                lo, hi = (base, True), (release_version(base.epoch, nxt), False)\n"
            "            elif op == \">=\":\n"
            "                lo = (Version(ver), True)\n"
            "            elif op == \">\":\n"
            "                lo = (Version(ver), False)\n"
            "            elif op == \"<=\":\n"
            "                hi = (Version(ver), True)\n"
            "            elif op == \"<\":\n"
            "                hi = (Version(ver), False)\n"
            "            if lo is not None and (\n"
            "                lower is None\n"
            "                or lo[0] > lower[0]\n"
            "                or (lo[0] == lower[0] and not lo[1])\n"
            "            ):\n"
            "                lower = lo\n"
            "            if hi is not None and (\n"
            "                upper is None\n"
            "                or hi[0] < upper[0]\n"
            "                or (hi[0] == upper[0] and not hi[1])\n"
            "            ):\n"
            "                upper = hi\n"
            "        return lower, upper\n\n"
            "    def __len__(self) -> int:\n        \"\"\"Returns the number of specifiers in this specifier set.\"\"\"\n")


SPECS = {
    "tags_platform_filter": dict(prompt=D_PROMPT, test=D_TEST, make=make_d, required=["src/packaging/utils.py", "src/packaging/tags.py"],
                                 regress=["tests/test_utils.py", "tests/test_tags.py"], type="A"),
    "metadata_extra_dupes": dict(prompt=E_PROMPT, test=E_TEST, make=make_e,
                                 required=["src/packaging/metadata.py", "src/packaging/markers.py", "src/packaging/_parser.py"],
                                 regress=["tests/test_metadata.py", "tests/test_markers.py"], type="B"),
    "specifier_bounds": dict(prompt=F_PROMPT, test=F_TEST, make=make_f, required=["src/packaging/specifiers.py", "src/packaging/version.py"],
                             regress=["tests/test_specifiers.py"], type="C"),
}


def main() -> int:
    only = sys.argv[1:] or list(SPECS)
    for task in only:
        s = SPECS[task]
        root = dev_copy(task)
        s["make"](root)
        changed = run("git", "diff", "--name-only", cwd=root).split()
        assert changed and all(c in s["required"] for c in changed), changed
        for c in changed:
            py_compile.compile(str(root / c), doraise=True)
        patch = run("git", "diff", "--no-color", cwd=root)
        out = TASKS / task
        (out / "private").mkdir(parents=True, exist_ok=True)
        (out / "prompt.md").write_text(s["prompt"], encoding="utf-8", newline="\n")
        (out / "private" / "ref.patch").write_text(patch, encoding="utf-8", newline="\n")
        (out / "private" / "test_x3_hidden.py").write_text(s["test"], encoding="utf-8", newline="\n")
        py_compile.compile(str(out / "private" / "test_x3_hidden.py"), doraise=True)
        (out / "task.json").write_text(json.dumps({
            "task": task, "commit": COMMIT, "required_files": s["required"], "regress": s["regress"],
            "hidden_test": "private/test_x3_hidden.py", "ref_patch": "private/ref.patch", "type": s["type"],
            "split": "confirm-only (11-19): 하네스 튜닝에 쓰지 않는다"}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        # 고정 커밋 원본에 깨끗이 붙는지 (원본 작업 트리는 바꾸지 않음)
        chk = subprocess.run(["git", "apply", "--check", str(out / "private" / "ref.patch")], cwd=SRC, capture_output=True, text=True)
        assert chk.returncode == 0, chk.stderr
        added = sum(1 for ln in patch.splitlines() if ln.startswith("+") and not ln.startswith("+++"))
        removed = sum(1 for ln in patch.splitlines() if ln.startswith("-") and not ln.startswith("---"))
        print(f"ok {task}: files {changed}, +{added} -{removed}, apply --check ok, compile ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
