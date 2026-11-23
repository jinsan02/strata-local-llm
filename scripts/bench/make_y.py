"""Y 세트 만들기: work/stage/y/ytasks 의 과제 파일 + 아래 편집 정의로 setup · ref · 돌연변이 패치를 만들어 configs/eval/y-set 에 둔다.
패치는 고정 커밋 사본에 문자열 편집(정확히 1번 일치)을 하고 git diff 로 뽑는다. 지시문의 {ACTUAL_*} · {FAIL_LOG} 는 버그를 심은 사본에서 실제 출력으로 채운다.
측정 체인이 없을 때만 돌린다. python make_y.py"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

NL = chr(10)
B = chr(92)
STAGE = Path("C:/strata-lab/work/stage/y/ytasks")
OUT = Path("C:/strata-lab/configs/eval/y-set")
WORK = Path("C:/strata-lab/work/y-make")
REPOS = {"packaging": ("C:/strata-lab/work/packaging-src", "6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc", "C:/ProgramData/anaconda3/envs/x3_packaging/python.exe"),
         "flask": ("C:/strata-lab/work/swe/pallets__flask-5014-src", "7ee9ceb71e868944a46e1ff00b506772a53a4f1d","C:/ProgramData/anaconda3/envs/swe_flask_5014/python.exe")}


def clone(name, repo):
    src, commit, _ = REPOS[repo]
    d = WORK / name
    if d.exists():
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(d)], capture_output=True)
    WORK.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--no-checkout", src, str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "-c", "core.autocrlf=false", "checkout", "-q", "--detach", commit], check=True)
    return d


def edit(root, path, old, new):
    p = root / path
    t = p.read_bytes().decode("utf-8")
    assert chr(13) not in t, (path, "CRLF in working tree")
    n = t.count(old)
    assert n == 1, (path, n, old[:80])
    p.write_bytes(t.replace(old, new, 1).encode("utf-8"))


def diff(root):
    r = subprocess.run(["git", "-C", str(root), "diff", "--no-color"], capture_output=True, check=True)
    out = r.stdout.decode("utf-8")
    assert out.strip(), "empty diff"
    return out


def commit_all(root, msg):
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=y", "-c", "user.email=y@localhost", "commit", "-q", "-m", msg], check=True)


def make_patch(repo, name, edits, base_edits=()):
    """base_edits 를 커밋한 상태에서 edits 를 적용한 diff."""
    d = clone(name, repo)
    if base_edits:
        for e in base_edits:
            edit(d, *e)
        commit_all(d, "base")
    for e in edits:
        edit(d, *e)
    out = diff(d)
    subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(d)], capture_output=True)
    return out


def run_py(repo, root, args):
    py = REPOS[repo][2]
    env = {**os.environ, "PYTHONPATH": str(root / "src"), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}
    return subprocess.run([py, *args], cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)


# ── 편집 정의 ────────────────────────────────────────────────────────────────
Y1_BUG = [("src/packaging/version.py", "    if pre is None and post is None and dev is not None:", "    if pre is None and dev is not None:")]
Y2_BUG = [("src/packaging/utils.py", '_build_tag_regex = re.compile(r"(' + B + 'd+)(.*)' + B + 'Z", re.ASCII)',
           '_build_tag_regex = re.compile(r"(' + B + 'd+?)(.*)' + B + 'Z", re.ASCII)')]

U = "src/packaging/utils.py"
V = "src/packaging/version.py"
Y3_MUTANTS = {
    "m01_strip_default": [(U, "version: Version | str, *, strip_trailing_zero: bool = True", "version: Version | str, *, strip_trailing_zero: bool = False")],
    "m02_invalid_empty": [(U, "        except InvalidVersion:" + NL + "            return str(version)", "        except InvalidVersion:" + NL + '            return ""')],
    "m03_ignore_flag": [(U, "    return str(version._trim_release() if strip_trailing_zero else version)", "    return str(version._trim_release())")],
    "m04_trim_all_zeros": [(V, "        while i > 1 and release[i - 1] == 0:", "        while i > 0 and release[i - 1] == 0:")],
    "m05_drop_local": [(V, "        new_version._local = self._local", "        new_version._local = None")],
    "m06_drop_pre": [(V, "        new_version._pre = self._pre", "        new_version._pre = None")],
    "m07_drop_post": [(V, "        new_version._post = self._post", "        new_version._post = None")],
    "m08_drop_epoch": [(V, "        new_version._epoch = self._epoch", "        new_version._epoch = 0")],
    "m09_trim_one_zero": [(V, "        while i > 1 and release[i - 1] == 0:" + NL + "            i -= 1", "        if i > 1 and release[i - 1] == 0:" + NL + "            i -= 1")],
    "m10_drop_dev": [(V, "        new_version._dev = self._dev", "        new_version._dev = None")],
}

Y4_HELPER = NL.join([
    "def _parse_filename_version(",
    "    version_part: str, filename: str, *, error: type[ValueError], kind: str",
    ") -> Version:",
    '    """Parse the version part of a distribution filename.',
    "",
    "    :class:`~packaging.version.InvalidVersion` is re-raised as **error**.",
    '    """',
    "    try:",
    "        return Version(version_part)",
    "    except InvalidVersion as e:",
    '        raise error(f"Invalid {kind} filename (invalid version): {filename!r}") from e',
])
Y4_REF = [
    (U, NL + NL + "def canonicalize_name(", NL + NL + Y4_HELPER + NL + NL + NL + "def canonicalize_name("),
    (U, NL.join(["    try:", "        version = Version(parts[1])", "    except InvalidVersion as e:", "        raise InvalidWheelFilename(",
                 '            f"Invalid wheel filename (invalid version): {filename!r}"', "        ) from e"]),
     NL.join(["    version = _parse_filename_version(", '        parts[1], filename, error=InvalidWheelFilename, kind="wheel"', "    )"])),
    (U, NL.join(["    try:", "        version = Version(version_part)", "    except InvalidVersion as e:", "        raise InvalidSdistFilename(",
                 '            f"Invalid sdist filename (invalid version): {filename!r}"', "        ) from e"]),
     NL.join(["    version = _parse_filename_version(", '        version_part, filename, error=InvalidSdistFilename, kind="sdist"', "    )"])),
]

Y5_METHOD = NL.join([
    "",
    '    def get_cookie_max_age(self, app: "Flask") -> t.Optional[int]:',
    '        """The ``Max-Age`` of the session cookie in seconds, from the',
    "        :data:`SESSION_COOKIE_MAX_AGE` config. ``None`` means the cookie has no",
    "        ``Max-Age``.",
    '        """',
    "        from datetime import timedelta",
    "",
    '        value = app.config["SESSION_COOKIE_MAX_AGE"]',
    "        if value is None:",
    "            return None",
    "        if isinstance(value, timedelta):",
    "            seconds = int(value.total_seconds())",
    "        elif isinstance(value, int) and not isinstance(value, bool):",
    "            seconds = value",
    "        else:",
    "            raise TypeError(",
    '                "SESSION_COOKIE_MAX_AGE must be an int, a timedelta, or None."',
    "            )",
    "        if seconds < 0:",
    '            raise ValueError("SESSION_COOKIE_MAX_AGE must not be negative.")',
    "        return seconds",
])
Y5_REF = [
    ("src/flask/app.py", '            "SESSION_COOKIE_SAMESITE": None,' + NL, '            "SESSION_COOKIE_SAMESITE": None,' + NL + '            "SESSION_COOKIE_MAX_AGE": None,' + NL),
    ("src/flask/sessions.py", '        return app.config["SESSION_COOKIE_SAMESITE"]' + NL,
     '        return app.config["SESSION_COOKIE_SAMESITE"]' + NL + Y5_METHOD + NL),
    ("src/flask/sessions.py", "            expires=expires," + NL, "            expires=expires," + NL + "            max_age=self.get_cookie_max_age(app)," + NL),
]

Y6_METHOD = NL.join([
    "    def require(self, *keys: str, allow_none: bool = False) -> dict[str, t.Any]:",
    '        """Return the values of the given keys, raising :exc:`KeyError` that',
    "        lists every missing key (sorted) if any are missing. A value of",
    "        ``None`` counts as missing unless **allow_none** is true.",
    '        """',
    "        if not keys:",
    '            raise TypeError("require() needs at least one key")',
    "        for key in keys:",
    "            if not isinstance(key, str):",
    '                raise TypeError(f"config keys must be str, not {type(key).__name__}")',
    "        missing = sorted(",
    "            {k for k in keys if k not in self or (self[k] is None and not allow_none)}",
    "        )",
    "        if missing:",
    """            raise KeyError(f"Missing required config keys: {', '.join(missing)}")""",
    "        return {k: self[k] for k in keys}",
    "",
])
Y6_REF = [("src/flask/config.py", "    def __repr__(self) -> str:", Y6_METHOD + "    def __repr__(self) -> str:")]


def put(task, rel, text):
    p = OUT / task / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))


def copy_stage(task):
    src = STAGE / task
    dst = OUT / task
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    # Y1: 버그 심기 + 보고서 출력 채우기
    t = "y1_version_postdev_order"
    copy_stage(t)
    put(t, "private/setup.patch", make_patch("packaging", "y1-setup", Y1_BUG))
    d = clone("y1-bug", "packaging")
    for e in Y1_BUG:
        edit(d, *e)
    r = run_py("packaging", d, ["-c", "from packaging.version import Version; from packaging.specifiers import SpecifierSet; "
                                "print(repr(sorted(['1.0', '1.0a1', '1.0.post1.dev2', '1.0.post1'], key=Version))); "
                                "print(SpecifierSet('>=1.0', prereleases=True).contains('1.0.post1.dev2'))"])
    assert r.returncode == 0, r.stderr
    act_sorted, act_contains = r.stdout.strip().splitlines()
    commit_all(d, "bug")
    for e in Y1_BUG:   # 되돌리기 = 참조 패치
        edit(d, e[0], e[2], e[1])
    put(t, "private/ref.patch", diff(d))
    pm = (OUT / t / "prompt.md").read_text(encoding="utf-8")
    pm = pm.replace("{ACTUAL_SORTED}", act_sorted).replace("{ACTUAL_CONTAINS}", act_contains)
    put(t, "prompt.md", pm)
    print(t, "actual:", act_sorted, act_contains)

    # Y2: 버그 심기 + 실패 로그 채우기
    t = "y2_wheel_build_number"
    copy_stage(t)
    put(t, "private/setup.patch", make_patch("packaging", "y2-setup", Y2_BUG))
    d = clone("y2-bug", "packaging")
    for e in Y2_BUG:
        edit(d, *e)
    r = run_py("packaging", d, ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "--tb=short", "tests/test_utils.py"])
    assert r.returncode != 0, "Y2: 버그를 심었는데 test_utils 가 통과한다"
    out = r.stdout.replace(str(d).replace(B, "/"), ".").replace(str(d), ".")
    lines = out.splitlines()
    k = next(i for i, l in enumerate(lines) if "FAILURES" in l)
    log = NL.join(lines[k:k + 60]).rstrip()
    commit_all(d, "bug")
    for e in Y2_BUG:
        edit(d, e[0], e[2], e[1])
    put(t, "private/ref.patch", diff(d))
    pm = (OUT / t / "prompt.md").read_text(encoding="utf-8").replace("{FAIL_LOG}", log)
    put(t, "prompt.md", pm)
    print(t, "log lines", len(log.splitlines()))

    # Y3: 돌연변이
    t = "y3_tests_canonicalize_version"
    copy_stage(t)
    for name, eds in Y3_MUTANTS.items():
        put(t, f"private/mutants/{name}.patch", make_patch("packaging", f"y3-{name}", eds))
    print(t, "mutants", len(Y3_MUTANTS))

    # Y4 · Y5 · Y6: 참조 패치
    for t, repo, eds in (("y4_refactor_filename_version", "packaging", Y4_REF), ("y5_session_cookie_max_age", "flask", Y5_REF),
                         ("y6_config_require", "flask", Y6_REF)):
        copy_stage(t)
        put(t, "private/ref.patch", make_patch(repo, f"{t}-ref", eds))
        print(t, "ref ok")
    for leftover in WORK.glob("*"):
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(leftover)], capture_output=True)


if __name__ == "__main__":
    main()
