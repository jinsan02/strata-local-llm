"""X3 교차 확인 — SWE-bench Verified 2건을 도구 탐색(navigate)으로 푼다. 로컬 재현 채점 (공식 Docker 하니스 아님).

    python scripts/bench/run_swe.py [--instances pallets__flask-5014 pytest-dev__pytest-8399]

모델 입력: problem_statement 와 도구(list_files · grep · read_file)뿐. 정답 패치 · 힌트(hints_text) · 새 테스트는 넣지 않는다.
채점: 모델 편집 적용 -> test.patch 적용 -> FAIL_TO_PASS · PASS_TO_PASS 실행. 원장 workload = swe-verified-<id> (packaging 과제와 따로 집계).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_bench as rb  # noqa: E402
import run_x3 as x3  # noqa: E402

CASES = rb.ROOT / "configs" / "eval" / "swe-verified"
WORK = Path(r"C:\strata-lab\work\swe")
ENVS = Path(r"C:\ProgramData\anaconda3\envs")


def fresh(iid: str, base: str, name: str) -> Path:
    d = WORK / name
    if d.exists():
        shutil.rmtree(d, onerror=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
    subprocess.run(["git", "clone", "-q", "--no-checkout", str(WORK / f"{iid}-src"), str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "checkout", "-q", base], check=True)
    return d


def apply_edits(root: Path, answer: str):
    blocks = x3.EDIT_RE.findall(answer or "")
    errors, applied = [], 0
    for path, search, replace in blocks:
        p = (root / path).resolve()
        parts = Path(path).parts
        if root.resolve() not in p.parents or "tests" in parts or "testing" in parts:
            errors.append(f"{path}: 허용되지 않는 경로")
            continue
        if not p.exists() and search.strip():
            errors.append(f"{path}: 파일 없음")
            continue
        if not search.strip():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(replace + "\n", encoding="utf-8", newline="\n")
            applied += 1
            continue
        text = p.read_text(encoding="utf-8")
        n = text.count(search)
        if n != 1:
            errors.append(f"{path}: SEARCH 일치 {n}회")
            continue
        p.write_text(text.replace(search, replace, 1), encoding="utf-8", newline="\n")
        applied += 1
    if not blocks:
        errors.append("편집 블록 없음")
    return applied, errors


def grade(root: Path, case: dict, py: str) -> dict:
    subprocess.run(["git", "-C", str(root), "apply", str(CASES / case["instance_id"] / "private" / "test.patch")], check=True)
    t0 = time.perf_counter()
    r = subprocess.run([py, "-m", "pytest", "-rA", "-p", "no:cacheprovider", *case["test_files"]], cwd=root,
                       capture_output=True, text=True, timeout=1800)
    ms = (time.perf_counter() - t0) * 1000
    st = {}
    for line in (r.stdout + r.stderr).splitlines():
        if m := re.match(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+(\S+)", line):
            st[m.group(2)] = m.group(1)
    f2p = sum(st.get(i) == "PASSED" for i in case["FAIL_TO_PASS"])
    p2p = sum(st.get(i) == "PASSED" for i in case["PASS_TO_PASS"])
    return {"f2p": f"{f2p}/{len(case['FAIL_TO_PASS'])}", "p2p": f"{p2p}/{len(case['PASS_TO_PASS'])}",
            "resolved": f2p == len(case["FAIL_TO_PASS"]) and p2p == len(case["PASS_TO_PASS"]), "tests_ms": ms}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", nargs="+", default=["pallets__flask-5014", "pytest-dev__pytest-8399"])
    ap.add_argument("--ctx", type=int, default=32768)
    ap.add_argument("--budget", type=int, default=8192)
    ap.add_argument("--max-steps", type=int, default=16)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--prefix", default="x3s")
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--timeout", type=float, default=1800)
    a = ap.parse_args()
    api_key = os.environ.get("STRATA_API_KEY", "strata-local")
    engine_dir = Path(r"C:\strata-lab\engine")
    server_cfg = json.loads((engine_dir / f"strata-qwen36-ctx{a.ctx}.json").read_text(encoding="utf-8"))
    engine_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=engine_dir, capture_output=True, text=True).stdout.strip()
    env = {"engine_commit": engine_commit, "engine_exe_sha256": rb.sha256_bytes(Path(server_cfg["exe"]).read_bytes()), "harness": "local conda"}
    env_sha = rb.sha256_bytes(rb.canon(env))
    commit, dirty = rb.git("rev-parse", "HEAD"), "1" if rb.git("status", "--porcelain") else "0"
    k = a.ctx // 1024
    for iid in a.instances:
        case = json.loads((CASES / iid / "instance.json").read_text(encoding="utf-8"))
        py = str(ENVS / case["env"] / "python.exe")
        for i in range(1, a.repeat + 1):
            name = f"{a.prefix}_m0_e0_s0_ctx{k}k_nav_{iid.replace('__', '_').replace('-', '_')}"
            run_dir = rb.ROOT / "experiments" / "runs" / name
            run_dir.mkdir(parents=True, exist_ok=True)
            root = fresh(iid, case["base_commit"], f"{name}_r{i}")
            sys_txt = (f"너는 {case['repo']} 저장소(커밋 {case['base_commit'][:12]})에서 이슈를 고치는 코딩 에이전트다. 파일은 미리 주어지지 않는다. "
                       "list_files · grep · read_file 도구로 관련 코드를 찾아 읽은 뒤, 마지막 답변에 편집 블록으로 수정을 제시하라. 테스트 파일은 고치지 마라.")
            msgs = [{"role": "system", "content": sys_txt},
                    {"role": "user", "content": "### 이슈\n" + case["problem_statement"] + "\n\n" + x3.FORMAT}]
            cfg = {"instance": iid, "dataset_revision": case["dataset_revision"], "base_commit": case["base_commit"], "mode": "navigate",
                   "tools": x3.TOOLS, "max_steps": a.max_steps, "budget": a.budget, "sampling": rb.SAMPLING, "server_config": server_cfg,
                   "harness": "local conda, not official Docker"}
            cfg_sha = rb.sha256_bytes(rb.canon(cfg))
            (run_dir / "config.json").write_bytes(rb.canon(cfg))
            (run_dir / "env.json").write_bytes(rb.canon(env))
            tool_log, model_ms, tool_ms, out_tok, last_in, final, status = [], 0.0, 0.0, 0, 0, "", "ok"
            for step in range(a.max_steps):
                force = step == a.max_steps - 1 or last_in > 24320 - 2048
                if force:
                    msgs.append({"role": "user", "content": "이제 도구를 더 쓰지 말고 편집 블록으로 답하라."})
                try:
                    mt = max(1024, min(a.budget, a.ctx - last_in - 2048)) if last_in else a.budget
                    data, ms = x3.chat_once(a.base_url, api_key, msgs, mt, a.timeout, None if force else x3.TOOLS)
                except Exception as ex:  # noqa: BLE001
                    status, final = "fail", f"요청 실패: {ex}"
                    break
                model_ms += ms
                u = data.get("usage") or {}
                last_in = u.get("prompt_tokens") or last_in
                out_tok += u.get("completion_tokens") or 0
                msg = data["choices"][0]["message"]
                calls = msg.get("tool_calls") or []
                if not calls:
                    final = msg.get("content") or ""
                    break
                msgs.append({"role": "assistant", "content": msg.get("content") or "", "tool_calls": calls})
                for c in calls:
                    try:
                        args = json.loads(c["function"].get("arguments") or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    t0 = time.perf_counter()
                    out = x3.run_tool(root, c["function"]["name"], args)
                    tool_ms += (time.perf_counter() - t0) * 1000
                    tool_log.append({"step": step, "tool": c["function"]["name"], "args": args, "out_chars": len(out)})
                    msgs.append({"role": "tool", "tool_call_id": c.get("id", ""), "content": out[:12000]})
            gold_files = [l.split(" b/")[-1] for l in (CASES / iid / "private" / "gold.patch").read_text(encoding="utf-8").splitlines()
                          if l.startswith("diff --git")]
            read = {t["args"].get("path") for t in tool_log if t["tool"] == "read_file"}
            found = [f for f in gold_files if f in read]
            applied, errs = x3.apply_edits(root, final, sorted(p for p in read if p), deny=("tests", "testing"))
            fmt = x3.fmt_note()
            gr = grade(root, case, py) if applied else None
            et = ("no_edit" if any("편집 블록 없음" in e for e in errs) else "apply_fail" if not applied else
                  "pass" if gr["resolved"] else "test_fail")
            row = {"run_id": f"{name}_r{i}", "config_id": "X3", "phase": "eval", "origin": "local", "workload": f"swe-verified-{iid}",
                   "model_id": "M0", "model_sha256": x3.M0_SHA, "engine_commit": engine_commit, "settings_id": "S0", "ctx": a.ctx,
                   "parallel": 1, "kv": "fp32", "mtp": "on", "thinking": "on", "cache_state": "cold", "git_commit": commit,
                   "git_dirty": dirty, "config_sha256": cfg_sha, "env_sha256": env_sha,
                   "ts_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "status": status,
                   "input_tokens": last_in, "max_tokens": a.budget, "output_tokens": out_tok, "answer_reached": 1 if final.strip() else 0,
                   "tests_passed": gr["f2p"] if gr else f"0/{len(case['FAIL_TO_PASS'])}", "total_ms": round(model_ms, 1),
                   "note": (f"SWE-bench Verified {iid} rev {case['dataset_revision'][:8]}; LOCAL harness (not official Docker); navigate "
                            f"{len(tool_log)} tool calls; gold-patch files read {len(found)}/{len(gold_files)}; edits {applied} "
                            f"({'; '.join(errs) or 'ok'}); F2P {gr['f2p'] if gr else 'NA'}; P2P {gr['p2p'] if gr else 'NA'}; "
                            f"resolved {gr['resolved'] if gr else False}; error_type {et}; {fmt}; model_ms {model_ms:.0f}; tool_exec_ms {tool_ms:.0f}; "
                            f"tests_ms {gr['tests_ms'] if gr else 0:.0f}; usage summed over turns")}
            rb.write_row(row)
            (run_dir / f"answer_r{i}.md").write_text(final, encoding="utf-8")
            (run_dir / f"tools_r{i}.json").write_text(json.dumps(tool_log, ensure_ascii=False, indent=1), encoding="utf-8")
            print(json.dumps({"run": row["run_id"], "tool_calls": len(tool_log), "gold_files_read": f"{len(found)}/{len(gold_files)}",
                              "error_type": et, "f2p": gr["f2p"] if gr else None, "p2p": gr["p2p"] if gr else None}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
