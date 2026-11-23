"""X4 채점: 노트북 클라이언트(Claude Code · Codex)가 만든 diff 를 본체에서 X3 · Y 와 같은 채점기로 본다.
과제 사본(setup_patch 포함)을 새로 만들고 diff 를 적용한 뒤 grade() → 숨은 테스트 · 회귀 · 통과. 결과는 work/x4/results.jsonl 에 한 줄.
숨은 테스트 · 참조 패치는 노트북으로 보내지 않는다(채점은 본체에서만).

    python scripts/bench/x4_grade.py <set:x3|y> <task> <diff 파일> <run 이름> [--client claude|codex|worker] [--meta meta.json]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_x3 as X  # noqa: E402

OUT = Path("C:/strata-lab/work/x4")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_set", choices=["x3", "y"])
    ap.add_argument("task")
    ap.add_argument("diff")
    ap.add_argument("run")
    ap.add_argument("--client", default="claude")
    ap.add_argument("--meta", default=None, help="클라이언트 쪽 기록(시간 · 턴 · 토큰) JSON")
    a = ap.parse_args()
    a.diff = str(Path(a.diff).resolve())   # git apply 는 작업 복사본에서 돌므로 절대 경로로
    X.TASKS = X.TASK_SETS[a.task_set]
    tcfg = json.loads((X.TASKS / a.task / "task.json").read_text(encoding="utf-8"))
    X.use_repo(tcfg.get("repo", "packaging"))
    X.WRITE_ALLOW = set(tcfg.get("write_allow", []))
    setup = (X.TASKS / a.task / tcfg["setup_patch"]) if tcfg.get("setup_patch") else None
    root = X.fresh_copy(f"x4-{a.run}", setup)
    diff = Path(a.diff).read_text(encoding="utf-8", errors="replace")
    touched = sorted(set(re.findall(r"^\+\+\+ b/(\S+)", diff, flags=re.M)))
    bad = [p for p in touched if p.startswith("tests/") and p not in X.WRITE_ALLOW]
    res = {"run": a.run, "client": a.client, "task_set": a.task_set, "task": a.task, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "touched": touched, "tests_touched": bad}
    if not diff.strip():
        res.update({"applied": False, "error_type": "no_edit"})
    else:
        # 테스트 파일 수정은 채점 전에 버린다(과제 규칙: 테스트 파일은 고치지 않는다). 버린 경로는 tests_touched 로 남긴다
        args = ["git", "apply", "--whitespace=nowarn"] + [f"--exclude={p}" for p in bad] + [a.diff]
        ap_ = subprocess.run(args, cwd=root, capture_output=True, text=True)
        res["applied"] = ap_.returncode == 0
        if not res["applied"]:
            res.update({"error_type": "apply_fail", "apply_err": ap_.stderr[-400:]})
    if res.get("applied"):
        if tcfg.get("grade") == "mutants":
            total = len(list((X.TASKS / a.task / "private" / "mutants").glob("*.patch")))
        else:   # run_x3 와 같이 수집 수로 센다(매개변수화 포함)
            probe = X.fresh_copy(f"x4-{a.run}-count", setup)
            (probe / "tests" / "test_x3_hidden.py").write_bytes((X.TASKS / a.task / "private" / "test_x3_hidden.py").read_bytes())
            c = subprocess.run([X.PYX, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "tests/test_x3_hidden.py"],
                               cwd=probe, capture_output=True, text=True, env={**__import__("os").environ, "PYTHONPATH": str(probe / "src")})
            m = re.search(r"(\d+) tests? collected", c.stdout)
            total = int(m.group(1)) if m else 0
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(probe)], capture_output=True)
        gr = X.grade(root, tcfg, total)
        res.update({"hidden": gr["hidden"], "regress": gr["regress"], "ok": gr["ok"], "error_type": X.error_type(1, [], gr)})
    if a.meta and Path(a.meta).is_file():
        res["client_meta"] = json.loads(Path(a.meta).read_text(encoding="utf-8", errors="replace"))
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "results.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False) + chr(10))
    print(json.dumps({k: v for k, v in res.items() if k != "client_meta"}, ensure_ascii=False))
    subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(root)], capture_output=True)
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
