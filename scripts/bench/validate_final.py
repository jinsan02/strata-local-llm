"""F1 최종 평가 과제 검증 (docs/final-eval-spec-20261124.md 5절 V1~V7).

분리 규칙(S2): 화면에는 과제 ID · 통과 여부 · 실패한 검사 번호만 낸다. 과제 내용 · 테스트 출력 · 패치는 화면에 내지 않고
final_eval/_validation/<과제ID>.json 에만 쓴다(그 파일은 Codex 와 사람만 본다).

    python validate_final.py                 # final_eval 아래 모든 과제
    python validate_final.py <과제ID> ...     # 일부만
    python validate_final.py --root <폴더>    # selftest 용 (final_eval 대신 다른 폴더)

과제 폴더: <root>/<저장소>/<과제ID>/{task.json, prompt.md, private/...}. 저장소 → bundle · 커밋은 task.json 의 repo · commit.
CPU 를 쓰므로 측정 체인이 없을 때만 돌린다.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

LAB = Path("C:/strata-lab")
BUNDLES = LAB / "work" / "final" / "bundles"          # <repo>.bundle
PY = os.environ.get("FINAL_PY", "C:/ProgramData/anaconda3/envs/final_eval/python.exe")
TIME_LIMIT = 60.0


def run(cmd, cwd, env=None, timeout=300):
    t = time.time()
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, (r.stdout + r.stderr)[-4000:], time.time() - t
    except subprocess.TimeoutExpired:
        return 99, "timeout", time.time() - t


def git(root, *a):
    return run(["git", "-C", str(root), "-c", "core.autocrlf=false", *a], cwd=root)


def fresh(cfg: dict, tdir: Path, work: Path, bundles: Path) -> tuple[bool, str]:
    """고정 커밋 사본 + setup.patch (V1)."""
    b = bundles / f"{cfg['repo']}.bundle"
    if not b.is_file():
        return False, f"bundle 없음: {b.name}"
    rc, out, _ = run(["git", "clone", "-q", "--no-checkout", str(b), str(work)], cwd=work.parent)
    if rc:
        return False, "clone 실패: " + out[-300:]
    rc, out, _ = git(work, "checkout", "-q", "--detach", cfg["commit"])
    if rc:
        return False, "checkout 실패: " + out[-300:]
    if cfg.get("setup_patch"):
        rc, out, _ = git(work, "apply", str(tdir / cfg["setup_patch"]))
        if rc:
            return False, "setup.patch 적용 실패: " + out[-300:]
    return True, ""


def pytest(work: Path, files: list[str], cfg: dict):
    pp = str(work / cfg.get("pythonpath", "src")) if cfg.get("pythonpath", "src") != "." else str(work)
    env = {**os.environ, "PYTHONPATH": pp, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):   # 네트워크 없는 테스트여야 한다
        env[k] = "http://127.0.0.1:9"
    return run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "-p", "no:randomly", *files], cwd=work, env=env)


def counts(out: str) -> dict:
    import re
    c = {k: 0 for k in ("passed", "failed", "error", "errors")}
    for n, k in re.findall(r"(\d+) (passed|failed|errors?)", out):
        c[k] += int(n)
    c["error"] += c.pop("errors")
    return c


def check_hidden(cfg, tdir, bundles, tmp) -> dict:
    res = {"checks": {}, "notes": []}
    ck = res["checks"]
    work = tmp / "w1"
    ok, msg = fresh(cfg, tdir, work, bundles)
    ck["V1"] = ok
    if not ok:
        res["notes"].append(msg)
        return res
    # F2: prompt 의 자리표시를 기준 상태의 실제 pytest 출력으로 채운다(노트북 출제자는 Python 이 없어 출력을 만들 수 없다).
    #     task.json "prompt_fill": {"placeholder": "{{PYTEST_OUTPUT}}", "tests": ["tests/test_x.py", ...]}. 채운 내용은 화면에 내지 않는다.
    pf = cfg.get("prompt_fill")
    if pf:
        pm = tdir / "prompt.md"
        txt = pm.read_text(encoding="utf-8")
        if pf["placeholder"] in txt:
            rc_f, out_f, _ = pytest(work, list(pf["tests"]), cfg)
            body = out_f.replace(str(work).replace("\\", "/"), ".").replace(str(work), ".").strip()
            cmd = "$ python -m pytest -q " + " ".join(pf["tests"])
            pm.write_text(txt.replace(pf["placeholder"], "```\n" + cmd + "\n" + body[-3000:] + "\n```"), encoding="utf-8")
            res["filled"] = {"rc": rc_f}
            ck["V2f"] = rc_f == 1          # 채운 출력이 실제 실패여야 한다
        # 자리표시가 없으면 이미 채운 것(다시 검증할 때) — 그대로 둔다
    hid_src = tdir / cfg["hidden_test"]
    (work / "tests").mkdir(exist_ok=True)   # pluggy 는 testing/ 을 쓴다 - 숨은 테스트 자리는 항상 tests/
    shutil.copy(hid_src, work / "tests" / "test_x3_hidden.py")
    rc, out, _ = pytest(work, ["tests/test_x3_hidden.py"], cfg)
    c = counts(out)
    ck["V2"] = rc in (1, 2) and c["failed"] + c["error"] > 0   # 기능 과제는 수집 단계 import 오류(rc 2)도 실패로 본다
    res["base"] = {"rc": rc, **c, "tail": out[-1500:]}
    # 참조 패치
    rc_a, out_a, _ = git(work, "apply", str(tdir / cfg["ref_patch"]))
    if rc_a:
        ck["V3"] = False
        res["notes"].append("ref.patch 적용 실패: " + out_a[-300:])
        return res
    # 참조 패치가 고친 파일 = 패치 머리의 경로 (작업 트리 diff 는 setup 을 정확히 되돌리는 패치에서 비어 버린다)
    import re
    ref_txt = (tdir / cfg["ref_patch"]).read_text(encoding="utf-8", errors="replace")
    touched = sorted({m for m in re.findall(r"^\+\+\+ b/(\S+)", ref_txt, re.M)} - {"tests/test_x3_hidden.py"})
    pre = cfg.get("pythonpath", "src")
    ck["V4"] = all(p.startswith(pre + "/") or pre == "." and not p.startswith("tests/") for p in touched) and bool(touched)
    res["ref_touched"] = touched
    files = ["tests/test_x3_hidden.py", *cfg.get("regress", [])]
    runs = []
    for _ in range(2):   # V6: 두 번 같은가
        rc, out, dt = pytest(work, files, cfg)
        runs.append({"rc": rc, **counts(out), "sec": round(dt, 1), "tail": out[-1500:]})
    ck["V3"] = runs[0]["rc"] == 0 and runs[0]["failed"] == 0 and runs[0]["error"] == 0 and runs[0]["passed"] > 0
    ck["V5"] = max(r["sec"] for r in runs) <= TIME_LIMIT
    ck["V6"] = all(r[k] == runs[0][k] for r in runs for k in ("rc", "passed", "failed", "error"))
    res["ref_runs"] = runs
    return res


def check_mutants(cfg, tdir, bundles, tmp) -> dict:
    res = {"checks": {}, "notes": []}
    ck = res["checks"]
    work = tmp / "w1"
    ok, msg = fresh(cfg, tdir, work, bundles)
    ck["V1"] = ok
    if not ok:
        res["notes"].append(msg)
        return res
    tf = cfg["test_file"]
    shutil.copy(tdir / cfg["ref_test"], work / tf)
    base_rc, out, dt = pytest(work, [tf], cfg)
    rc = base_rc
    ck["V2"] = rc == 0          # 원본에서 참조 테스트 통과
    res["base"] = {"rc": rc, **counts(out), "sec": round(dt, 1), "tail": out[-1500:]}
    muts = sorted((tdir / "private" / "mutants").glob("*.patch"))
    killed, times = [], [dt]
    for m in muts:
        rc_a, out_a, _ = git(work, "apply", str(m))
        if rc_a:
            res["notes"].append(f"돌연변이 적용 실패: {m.name}")
            killed.append(None)
            continue
        rc, out, dt = pytest(work, [tf], cfg)
        times.append(dt)
        killed.append(rc != 0)
        git(work, "apply", "-R", str(m))
    res["mutants"] = {m.name: k for m, k in zip(muts, killed)}
    n = len(muts)
    km = int(cfg.get("kill_min", 0))
    ck["V3"] = n >= 8 and all(k is True for k in killed) and 0 < km < n
    ck["V4"] = Path(tf).parts[0] in ("tests", "testing") and cfg.get("write_allow") == [tf]   # pluggy 는 testing/
    ck["V5"] = max(times) <= TIME_LIMIT
    # V6: 원본 통과를 한 번 더
    rc2, out2, _ = pytest(work, [tf], cfg)
    ck["V6"] = rc2 == base_rc   # (rc 는 돌연변이 반복에서 덮이므로 base_rc 와 비교)
    res["recheck"] = {"rc": rc2, **counts(out2), "tail": out2[-800:]}
    # V7: 기존 테스트 파일을 그대로 쓰면 kill_min 미만
    src_t = cfg.get("copy_from")
    if not src_t:
        ck["V7"] = False
        res["notes"].append("task.json 에 copy_from(기존 테스트 파일) 없음")
    else:
        shutil.copy(work / src_t, work / tf)
        k2 = 0
        for m in muts:
            if git(work, "apply", str(m))[0]:
                continue
            k2 += pytest(work, [tf], cfg)[0] != 0
            git(work, "apply", "-R", str(m))
        res["copy_kills"] = k2
        ck["V7"] = k2 < km
    return res


def validate(tdir: Path, bundles: Path, outdir: Path) -> tuple[str, bool, list[str]]:
    cfg = json.loads((tdir / "task.json").read_text(encoding="utf-8"))
    tid = cfg.get("task", tdir.name)
    need = ["task", "type", "repo", "commit", "required_files", "regress"]
    missing = [k for k in need if k not in cfg] + ([] if (tdir / "prompt.md").is_file() else ["prompt.md"])
    with tempfile.TemporaryDirectory(prefix="vf_") as t:
        tmp = Path(t)
        res = check_mutants(cfg, tdir, bundles, tmp) if cfg.get("grade") == "mutants" else check_hidden(cfg, tdir, bundles, tmp)
    if missing:
        res["checks"]["V0"] = False
        res["notes"].append("빠진 필드: " + ", ".join(missing))
    bad = [k for k, v in sorted(res["checks"].items()) if not v]
    want = {"V1", "V2", "V3", "V4", "V5", "V6"} | ({"V7"} if cfg.get("grade") == "mutants" else set())
    bad += sorted(want - set(res["checks"]))
    res["task"], res["pass"], res["failed_checks"] = tid, not bad, bad
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{tid}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return tid, not bad, bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks", nargs="*")
    ap.add_argument("--root", default=str(LAB / "final_eval"))
    ap.add_argument("--bundles", default=str(BUNDLES))
    a = ap.parse_args()
    root = Path(a.root)
    dirs = sorted(p.parent for p in root.glob("*/*/task.json"))
    if a.tasks:
        dirs = [d for d in dirs if d.name in a.tasks]
    ok_n = 0
    for d in dirs:
        tid, ok, bad = validate(d, Path(a.bundles), root / "_validation")
        ok_n += ok
        print(f"{tid}: {'PASS' if ok else 'FAIL ' + ','.join(bad)}")   # 내용은 출력하지 않는다(S2)
    print(f"검증 {ok_n}/{len(dirs)} 통과 (자세한 기록: {root / '_validation'})")
    return 0 if ok_n == len(dirs) else 1


if __name__ == "__main__":
    sys.exit(main())
