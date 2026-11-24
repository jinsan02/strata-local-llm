"""validate_final.py 자체 점검: packaging bundle(튜닝용 저장소, F1 에 쓰지 않음)로 장난감 과제 3개를 임시 폴더에 만들어 검증한다.
  t_ok   : 버그 심기(canonicalize_name 의 '.' 처리 제거) → 숨은 테스트 실패, 참조 패치로 통과 → PASS 기대
  t_bad  : 참조 패치가 엉뚱한 곳을 고침 → FAIL(V3) 기대
  t_mut  : 돌연변이 8개 + 참조 테스트 → V1~V6 통과, V7 은 copy_kills < kill_min 과 일치 기대
실제 final_eval 은 건드리지 않는다. 측정 체인이 없을 때만.   python selftest_validate_final.py
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.environ.setdefault("FINAL_PY", "C:/ProgramData/anaconda3/envs/x3_packaging/python.exe")
sys.path.insert(0, str(HERE))
import validate_final as V  # noqa: E402

BUNDLE_SRC = Path("C:/strata-lab/work/x4/bundles/packaging.bundle")
COMMIT = "6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc"
F = "src/packaging/utils.py"
L_VALUE = '    value = name.lower().replace("_", "-").replace(".", "-")'
L_WHILE = '    while "--" in value:'
L_REPL = '        value = value.replace("--", "-")'
L_VALID = '    if validate and not _validate_regex.fullmatch(name):'


def sh(cwd, *a):
    r = subprocess.run(["git", "-C", str(cwd), "-c", "core.autocrlf=false", *a], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return r.stdout


def patch_of(repo: Path, edits: list[tuple[str, str]], out: Path):
    p = repo / F
    raw = p.read_bytes().decode("utf-8")
    s = raw
    for old, new in edits:
        assert s.count(old) == 1, old
        s = s.replace(old, new)
    p.write_bytes(s.encode("utf-8"))
    out.write_text(sh(repo, "diff"), encoding="utf-8")
    p.write_bytes(raw.encode("utf-8"))


def main():
    fails = 0
    with tempfile.TemporaryDirectory(prefix="stvf_") as t:
        t = Path(t)
        bundles = t / "bundles"; bundles.mkdir()
        (bundles / "pk.bundle").write_bytes(BUNDLE_SRC.read_bytes())
        repo = t / "repo"
        subprocess.run(["git", "clone", "-q", "--no-checkout", str(bundles / "pk.bundle"), str(repo)], check=True)
        sh(repo, "checkout", "-q", "--detach", COMMIT)
        root = t / "fe"
        base = {"repo": "pk", "commit": COMMIT, "required_files": [F], "regress": ["tests/test_utils.py"]}
        hidden = ("from packaging.utils import canonicalize_name\n\n"
                  "def test_dot():\n    assert canonicalize_name('oslo.concurrency') == 'oslo-concurrency'\n\n"
                  "def test_plain():\n    assert canonicalize_name('Django') == 'django'\n")
        bug = [(L_VALUE, '    value = name.lower().replace("_", "-")')]
        for tid, ref_edits in (("t_ok", [('    value = name.lower().replace("_", "-")', L_VALUE)]),
                               ("t_bad", [('    value = name.lower().replace("_", "-")', '    value = name.lower().replace("_", "-")  # no-op'),])):
            d = root / "pk" / tid; (d / "private").mkdir(parents=True)
            patch_of(repo, bug, d / "private" / "setup.patch")
            # 참조 패치는 setup 뒤 상태에서 만든다
            sh(repo, "apply", str(d / "private" / "setup.patch"))
            patch_of(repo, ref_edits, d / "private" / "ref.patch")
            sh(repo, "checkout", "-q", "--", F)
            (d / "private" / "test_x3_hidden.py").write_text(hidden, encoding="utf-8")
            (d / "prompt.md").write_text("장난감 과제\n", encoding="utf-8")
            (d / "task.json").write_text(json.dumps({**base, "task": tid, "type": "F2", "setup_patch": "private/setup.patch",
                                                     "hidden_test": "private/test_x3_hidden.py", "ref_patch": "private/ref.patch"}), encoding="utf-8")
        # 돌연변이 과제
        d = root / "pk" / "t_mut"; (d / "private" / "mutants").mkdir(parents=True)
        muts = [[(L_VALUE, '    value = name.replace("_", "-").replace(".", "-")')],
                [(L_VALUE, '    value = name.lower().replace(".", "-")')],
                [(L_VALUE, '    value = name.lower().replace("_", "-")')],
                [(L_WHILE, '    if "--" in value:')],
                [(L_REPL, '        value = value.replace("--", "")')],
                [(L_VALUE, '    value = name.upper().replace("_", "-").replace(".", "-")')],
                [(L_VALID, '    if validate and _validate_regex.fullmatch(name):')],
                [(L_VALUE, '    value = name.lower().replace("_", "-").replace(".", "_")')]]
        for i, m in enumerate(muts):
            patch_of(repo, m, d / "private" / "mutants" / f"m{i:02d}.patch")
        (d / "private" / "ref_test.py").write_text(
            "import pytest\nfrom packaging.utils import canonicalize_name, InvalidName\n\n"
            "@pytest.mark.parametrize('a,b', [('Django', 'django'), ('oslo.concurrency', 'oslo-concurrency'), ('a_b', 'a-b'),"
            " ('a---b', 'a-b'), ('A.B_C', 'a-b-c'), ('x--y', 'x-y')])\n"
            "def test_norm(a, b):\n    assert canonicalize_name(a) == b\n\n"
            "def test_validate():\n    assert canonicalize_name('ok-name', validate=True) == 'ok-name'\n"
            "    with pytest.raises(InvalidName):\n        canonicalize_name('-bad', validate=True)\n", encoding="utf-8")
        (d / "prompt.md").write_text("장난감 테스트 작성 과제\n", encoding="utf-8")
        tf = "tests/test_y_sf.py"
        (d / "task.json").write_text(json.dumps({**base, "task": "t_mut", "type": "F6", "grade": "mutants", "test_file": tf,
                                                 "write_allow": [tf], "kill_min": 6, "ref_test": "private/ref_test.py",
                                                 "copy_from": "tests/test_utils.py"}), encoding="utf-8")
        outv = root / "_validation"
        r_ok = V.validate(root / "pk" / "t_ok", bundles, outv)
        r_bad = V.validate(root / "pk" / "t_bad", bundles, outv)
        r_mut = V.validate(root / "pk" / "t_mut", bundles, outv)
        mj = json.loads((outv / "t_mut.json").read_text(encoding="utf-8"))
        cases = [("t_ok PASS", r_ok[1] is True),
                 ("t_bad FAIL 에 V3 포함", (not r_bad[1]) and "V3" in r_bad[2]),
                 ("t_mut V1~V6 통과", all(mj["checks"].get(k) for k in ("V1", "V2", "V3", "V4", "V5", "V6"))),
                 ("t_mut V7 = copy_kills < kill_min", mj["checks"].get("V7") == (mj.get("copy_kills", 99) < 6)),
                 ("화면 출력 없이 기록만", (outv / "t_ok.json").is_file())]
        for name, ok in cases:
            print("ok  " if ok else "FAIL", name)
            fails += not ok
        print("  (참고) t_bad:", r_bad[2], " t_mut copy_kills:", mj.get("copy_kills"), " mutants:", mj.get("mutants"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
