"""SWE-bench Verified 교차 확인 2건 — 로컬 재현 환경 준비 · 기준 실패 / 정답 통과 확인 (본체).

공식 하니스는 Docker(리눅스 이미지 swebench/sweb.eval.*)가 필요한데 본체에 Docker 가 없다 -> 로컬 conda 환경으로
재현하고 결과를 '로컬 재현(공식 하니스 아님)' 으로 따로 표시한다. 채점 기준은 데이터셋의 FAIL_TO_PASS · PASS_TO_PASS.
정답 패치(patch)는 검증에만 쓰고 configs/eval/swe-verified/<id>/private/ 에 둔다. 모델 입력에는 problem_statement 만.
"""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROWS = Path(r"C:\strata-lab\work\swe_verified_rows.json")
REVISION = "78f471bf655a3137b2e8a75af1501690ec009ec3"
OUT = Path(r"C:\strata-lab\configs\eval\swe-verified")
WORK = Path(r"C:\strata-lab\work\swe")
CONDA = r"C:\ProgramData\anaconda3\Scripts\conda.exe"
ENVS = Path(r"C:\ProgramData\anaconda3\envs")

SPEC = {
    "pallets__flask-5014": {"env": "swe_flask_5014", "python": "3.11", "url": "https://github.com/pallets/flask.git",
                            "install": [["-m", "pip", "install", "-r", "requirements/tests.txt"], ["-m", "pip", "install", "-e", "."]],
                            "test_files": ["tests/test_blueprints.py"]},
    "pytest-dev__pytest-8399": {"env": "swe_pytest_8399", "python": "3.9", "url": "https://github.com/pytest-dev/pytest.git",
                                "install": [["-m", "pip", "install", "-e", ".[testing]"]],
                                "test_files": ["testing/test_nose.py", "testing/test_unittest.py"]},
}


def L(v):
    return v if isinstance(v, list) else json.loads(v)


def sh(args, cwd=None, env=None, timeout=3600):
    r = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def run_tests(py, repo, files, ids):
    rc, out = sh([py, "-m", "pytest", "-rA", "-p", "no:cacheprovider", *files], cwd=repo, timeout=1800)
    status = {}
    for line in out.splitlines():
        m = re.match(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+(\S+)", line)
        if m:
            status[m.group(2)] = m.group(1)
    got = {i: status.get(i, "MISSING") for i in ids}
    return got, out


def main():
    rows = {r["instance_id"]: r for r in json.loads(ROWS.read_text(encoding="utf-8"))}
    report = {"dataset": "SWE-bench/SWE-bench_Verified", "revision": REVISION, "harness": "local conda (no Docker)", "instances": {}}
    for iid, sp in SPEC.items():
        r = rows[iid]
        d = OUT / iid
        (d / "private").mkdir(parents=True, exist_ok=True)
        (d / "private" / "gold.patch").write_text(r["patch"], encoding="utf-8", newline="\n")
        (d / "private" / "test.patch").write_text(r["test_patch"], encoding="utf-8", newline="\n")
        (d / "instance.json").write_text(json.dumps({
            "instance_id": iid, "repo": r["repo"], "base_commit": r["base_commit"], "version": r["version"],
            "dataset_revision": REVISION, "problem_statement": r["problem_statement"],
            "FAIL_TO_PASS": L(r["FAIL_TO_PASS"]), "PASS_TO_PASS": L(r["PASS_TO_PASS"]), "test_files": sp["test_files"],
            "official_image": r["image"], "env": sp["env"], "python": sp["python"], "install": sp["install"],
            "note": "hints_text 는 모델 입력에 넣지 않는다"}, ensure_ascii=False, indent=1), encoding="utf-8")
        # 저장소 + 환경
        src = WORK / f"{iid}-src"
        if not src.exists():
            sh(["git", "clone", "-q", sp["url"], str(src)])
        py = str(ENVS / sp["env"] / "python.exe")
        if not Path(py).exists():
            rc, out = sh([CONDA, "create", "-y", "-q", "-n", sp["env"], "-c", "conda-forge", "--override-channels", f"python={sp['python']}", "pip", "git"])
            print(iid, "conda", rc)
        val = WORK / f"{iid}-val"
        if val.exists():
            shutil.rmtree(val, onerror=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
        sh(["git", "clone", "-q", "--no-checkout", str(src), str(val)])
        sh(["git", "-C", str(val), "checkout", "-q", r["base_commit"]])
        logs = []
        for step in sp["install"]:
            rc, out = sh([py, *step], cwd=val)
            logs.append(f"$ python {' '.join(step)} -> {rc}\n{out[-1500:]}")
        rc, out = sh(["git", "-C", str(val), "apply", str(d / "private" / "test.patch")])
        ids = L(r["FAIL_TO_PASS"]) + L(r["PASS_TO_PASS"])
        base, base_out = run_tests(py, val, sp["test_files"], ids)
        rc, out = sh(["git", "-C", str(val), "apply", str(d / "private" / "gold.patch")])
        gold, gold_out = run_tests(py, val, sp["test_files"], ids)
        f2p, p2p = L(r["FAIL_TO_PASS"]), L(r["PASS_TO_PASS"])
        res = {"base_f2p_failing": sum(base[i] != "PASSED" for i in f2p), "base_p2p_passing": sum(base[i] == "PASSED" for i in p2p),
               "gold_f2p_passing": sum(gold[i] == "PASSED" for i in f2p), "gold_p2p_passing": sum(gold[i] == "PASSED" for i in p2p),
               "n_f2p": len(f2p), "n_p2p": len(p2p),
               "gold_p2p_not_passing": [i for i in p2p if gold[i] != "PASSED"][:20]}
        res["ok"] = res["base_f2p_failing"] == len(f2p) and res["gold_f2p_passing"] == len(f2p) and res["gold_p2p_passing"] == len(p2p)
        report["instances"][iid] = res
        (WORK / f"{iid}-setup.log").write_text("\n".join(logs) + "\n=== base\n" + base_out[-6000:] + "\n=== gold\n" + gold_out[-6000:], encoding="utf-8")
        print(iid, json.dumps(res, ensure_ascii=False))
    (OUT / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
