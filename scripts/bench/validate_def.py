"""X3 과제 검증: 기준 커밋에서 숨은 테스트 실패 · 회귀 통과, 참조 패치 적용 뒤 숨은 테스트 전부 통과 · 회귀 통과.

CPU 를 쓰므로 GPU 측정 체인이 없을 때만 돌린다(측정 중이면 거부). 결과는 configs/eval/x3-packaging/validation.json 에 과제별로 더한다.

    python scripts/bench/validate_def.py tags_platform_filter metadata_extra_dupes specifier_bounds
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "work" / "packaging-src"
WORK = ROOT / "work" / "x3-validate"
TASKS = ROOT / "configs" / "eval" / "x3-packaging"
PYX = r"C:\ProgramData\anaconda3\envs\x3_packaging\python.exe"
COMMIT = "6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc"
BENCH = re.compile(r"night-chain|matrix-[a-z0-9]+\.ps1|cache-chain|run_(x3|swe|bench|coding)\.py", re.I)


def measuring() -> str | None:
    ps = "Get-CimInstance Win32_Process | ForEach-Object { $_.CommandLine }"
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    return next((ln.strip()[:120] for ln in out.splitlines() if BENCH.search(ln) and "validate_def" not in ln), None)


def fresh(name: str) -> Path:
    d = WORK / name
    if d.exists():
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(d)], capture_output=True)
    WORK.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--no-checkout", str(SRC), str(d)], check=True)
    subprocess.run(["git", "checkout", "-q", "--detach", COMMIT], cwd=d, check=True)
    return d


def pytest(root: Path, files: list[str]) -> tuple[int, str]:
    r = subprocess.run([PYX, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", *files], cwd=root,
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONPATH": str(root / "src"), "PYTHONDONTWRITEBYTECODE": "1"})
    tail = [ln for ln in r.stdout.splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
    return r.returncode, (tail[-1].strip("= ") if tail else r.stdout[-600:])


def validate(task: str) -> dict:
    cfg = json.loads((TASKS / task / "task.json").read_text(encoding="utf-8"))
    hidden = TASKS / task / "private" / "test_x3_hidden.py"
    patch = TASKS / task / "private" / "ref.patch"
    base = fresh(f"{task}-base")
    shutil.copy(hidden, base / "tests" / "test_x3_hidden.py")
    bh_rc, bh = pytest(base, ["tests/test_x3_hidden.py"])
    br_rc, br = pytest(base, cfg["regress"])
    ref = fresh(f"{task}-ref")
    subprocess.run(["git", "apply", str(patch)], cwd=ref, check=True)
    shutil.copy(hidden, ref / "tests" / "test_x3_hidden.py")
    rh_rc, rh = pytest(ref, ["tests/test_x3_hidden.py"])
    rr_rc, rr = pytest(ref, cfg["regress"])
    ok = bh_rc != 0 and br_rc == 0 and rh_rc == 0 and rr_rc == 0 and "failed" not in rh
    for d in (base, ref):
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(d)], capture_output=True)
    return {"base_hidden": bh, "base_regress": br, "ref_hidden": rh, "ref_regress": rr, "ok": ok}


def main() -> int:
    busy = measuring()
    if busy:
        print(f"측정 중이라 돌리지 않는다: {busy}")
        return 2
    tasks = sys.argv[1:]
    vp = TASKS / "validation.json"
    val = json.loads(vp.read_text(encoding="utf-8"))
    assert val["commit"] == COMMIT
    for t in tasks:
        res = validate(t)
        val["tasks"][t] = res
        print(t, json.dumps(res, ensure_ascii=False), flush=True)
    vp.write_text(json.dumps(val, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    return 0 if all(val["tasks"][t]["ok"] for t in tasks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
