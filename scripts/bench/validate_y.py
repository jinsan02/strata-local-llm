"""Y 세트 검증: run_x3 의 실제 함수(fresh_copy · setup_patch · grade · grade_mutants)로
기준(버그를 심은 사본) 숨은 테스트 실패 · 참조 패치 통과 · 회귀 통과를 확인한다. Y3 는 참조 테스트가 돌연변이를 다 잡고,
약한 테스트는 기준 미달인지, 저장소 기존 테스트 파일을 그대로 쓰면 몇 개 잡는지 본다.
CPU 를 쓰므로 측정 체인이 없을 때만. 결과는 configs/eval/y-set/validation.json.

    python scripts/bench/validate_y.py [과제 ...]
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_x3 as X  # noqa: E402
from validate_def import measuring  # noqa: E402

YSET = X.TASK_SETS["y"]
NL = chr(10)


def rm(d: Path) -> None:
    subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(d)], capture_output=True)


def hidden_count(root: Path) -> int:
    c = subprocess.run([X.PYX, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "tests/test_x3_hidden.py"],
                       cwd=root, capture_output=True, text=True, env={**__import__("os").environ, "PYTHONPATH": str(root / "src")})
    import re
    m = re.search(r"(\d+) tests? collected", c.stdout)
    return int(m.group(1)) if m else -1


def validate(task: str) -> dict:
    X.TASKS = YSET
    tcfg = json.loads((YSET / task / "task.json").read_text(encoding="utf-8"))
    X.use_repo(tcfg.get("repo", "packaging"))
    setup = (YSET / task / tcfg["setup_patch"]) if tcfg.get("setup_patch") else None
    res: dict = {"repo": tcfg.get("repo", "packaging"), "commit": X.COMMIT}
    if tcfg.get("grade") == "mutants":
        n = len(list((YSET / task / "private" / "mutants").glob("*.patch")))
        tf = tcfg["test_file"]
        cases = {"ref_test": (YSET / task / tcfg["ref_test"]).read_text(encoding="utf-8"),
                 "weak_test": "from packaging.utils import canonicalize_version" + NL + NL + NL
                              + "def test_one():" + NL + '    assert canonicalize_version("1.0.0") == "1"' + NL,
                 "repo_test_utils": None}
        for name, body in cases.items():
            root = X.fresh_copy(f"yval-{task}-{name}", setup)
            if body is None:
                shutil.copy(root / "tests" / "test_utils.py", root / tf)
            else:
                (root / tf).write_text(body, encoding="utf-8", newline=NL)
            g = X.grade(root, tcfg, n)
            res[name] = {"ok": g["ok"], "killed": g["hidden"], "regress": g["regress"], "detail": g["log_full"].splitlines()[1:n + 1]}
            rm(root)
        res["ok"] = res["ref_test"]["ok"] and res["ref_test"]["killed"] == f"{n}/{n}" and not res["weak_test"]["ok"]
        return res
    base = X.fresh_copy(f"yval-{task}-base", setup)
    shutil.copy(YSET / task / "private" / "test_x3_hidden.py", base / "tests" / "test_x3_hidden.py")
    total = hidden_count(base)
    (base / "tests" / "test_x3_hidden.py").unlink()
    gb = X.grade(base, tcfg, total)
    ref = X.fresh_copy(f"yval-{task}-ref", setup)
    ap = subprocess.run(["git", "apply", str(YSET / task / "private" / "ref.patch")], cwd=ref, capture_output=True, text=True)
    gr = X.grade(ref, tcfg, total) if ap.returncode == 0 else None
    res.update({"hidden_total": total, "base_hidden": gb["hidden"], "base_regress": gb["regress"], "ref_apply": ap.returncode == 0 or ap.stderr[-300:],
                "ref_hidden": gr["hidden"] if gr else None, "ref_regress": gr["regress"] if gr else None})
    base_hidden_fail = gb["hidden"].split("/")[0] != gb["hidden"].split("/")[1]
    base_regress_ok = gb["regress_ok"] or tcfg.get("bug_task", False)
    res["ok"] = bool(gr and gr["ok"] and base_hidden_fail and base_regress_ok and total > 0)
    for d in (base, ref):
        rm(d)
    return res


def main() -> int:
    busy = measuring()
    if busy:
        print(f"측정 중이라 돌리지 않는다: {busy}")
        return 2
    tasks = sys.argv[1:] or sorted(p.name for p in YSET.iterdir() if (p / "task.json").is_file())
    vp = YSET / "validation.json"
    val = json.loads(vp.read_text(encoding="utf-8")) if vp.is_file() else {"tasks": {}}
    for t in tasks:
        r = validate(t)
        val["tasks"][t] = r
        print(t, json.dumps(r, ensure_ascii=False), flush=True)
    vp.write_text(json.dumps(val, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)
    return 0 if all(val["tasks"][t]["ok"] for t in tasks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
