"""코딩 과제 러너 — 출력·reasoning 예산 단계 시험(XB)과 X3 탐색.

    python scripts/bench/run_coding.py --ctx 32768 --budgets 2048 4096 8192 --tasks merge_intervals lru_cache

과제마다 같은 프롬프트를 예산별로 보내고, 원장에 한 행씩 쓴다:
최종 답변 도달(answer_reached), 실제 사용 토큰(output_tokens), finish_reason, 테스트 통과(tests_passed 통과/전체).
모델 답의 마지막 ```python 블록을 solution.py 로 저장해 고정 단위 테스트를 돌린다 (본체 conda pytest).
테스트·채점 기준은 configs/eval/explore-coding 에 고정되어 있다 — 결과를 보고 바꾸지 않는다 (RULES 3).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_bench as rb  # noqa: E402

TASKS = rb.ROOT / "configs" / "eval" / "explore-coding"
PY = sys.executable


def extract_code(answer: str) -> str | None:
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", answer, flags=re.S)
    return blocks[-1] if blocks else None


def run_tests(task: str, code: str | None) -> tuple[str, str]:
    """(통과/전체, 요약). 코드가 없으면 0/전체."""
    tests = TASKS / task / "test_solution.py"
    total = None
    with tempfile.TemporaryDirectory() as d:
        shutil.copy(tests, d)
        if code is None:
            collect = subprocess.run([PY, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", d],
                                     capture_output=True, text=True, timeout=120)
            m = re.search(r"(\d+) tests? collected", collect.stdout) or re.search(r"(\d+) errors?", collect.stdout)
            return (f"0/{m.group(1)}" if m else "0/NA"), "코드 블록 없음"
        Path(d, "solution.py").write_text(code, encoding="utf-8")
        try:
            r = subprocess.run([PY, "-m", "pytest", "-q", "--tb=line", "-p", "no:cacheprovider", d],
                               capture_output=True, text=True, timeout=300, cwd=d)
        except subprocess.TimeoutExpired:
            return "0/NA", "테스트 시간 초과(300s)"
        out = r.stdout + r.stderr
        passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", out)) else 0
        failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", out)) else 0
        errors = int(m.group(1)) if (m := re.search(r"(\d+) errors?", out)) else 0
        total = passed + failed + errors
        tail = out.strip().splitlines()[-1] if out.strip() else ""
        return f"{passed}/{total if total else 'NA'}", tail[:160]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ctx", type=int, required=True)
    ap.add_argument("--budgets", type=int, nargs="+", default=[2048, 4096, 8192])
    ap.add_argument("--tasks", nargs="+", default=sorted(p.name for p in TASKS.iterdir() if p.is_dir()))
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--config-id", default="XB")
    ap.add_argument("--prefix", default="xb")
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--timeout", type=float, default=1800)
    a = ap.parse_args()

    api_key = os.environ.get("STRATA_API_KEY", "strata-local")
    engine_dir = Path(r"C:\strata-lab\engine")
    cand = engine_dir / f"strata-qwen36-ctx{a.ctx}.json"
    server_cfg = json.loads((cand if cand.exists() else engine_dir / "strata-qwen36-ud-q4_k_xl.json").read_text(encoding="utf-8"))
    env = {"engine_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=engine_dir, capture_output=True, text=True).stdout.strip(),
           "engine_exe_sha256": rb.sha256_bytes(Path(server_cfg["exe"]).read_bytes()),
           "driver": subprocess.run(["nvidia-smi", "--query-gpu=driver_version,name", "--format=csv,noheader"],
                                    capture_output=True, text=True).stdout.strip()}
    env_sha = rb.sha256_bytes(rb.canon(env))
    commit, dirty = rb.git("rev-parse", "HEAD"), "1" if rb.git("status", "--porcelain") else "0"
    k = a.ctx // 1024

    for task in a.tasks:
        prompt = (TASKS / task / "prompt.md").read_text(encoding="utf-8")
        tests_sha = rb.sha256_bytes((TASKS / task / "test_solution.py").read_bytes())
        exact = (rb.stream_chat(a.base_url, api_key, prompt, 1, a.timeout).get("usage") or {}).get("prompt_tokens")
        for budget in a.budgets:
            if exact is not None and exact + budget > a.ctx:
                print(json.dumps({"task": task, "budget": budget, "skip": f"입력 {exact} + 예산 {budget} > ctx {a.ctx}"},
                                 ensure_ascii=False))
                continue
            run_id = f"{a.prefix}_m0_e0_s0_ctx{k}k_{task}_b{budget // 1024}k"
            cfg = {"task": task, "prompt_sha256": rb.sha256_bytes(prompt.encode("utf-8")), "tests_sha256": tests_sha,
                   "budget": budget, "ctx": a.ctx, "sampling": rb.SAMPLING, "server_config": server_cfg,
                   "prompt_tokens_exact": exact}
            config_sha = rb.sha256_bytes(rb.canon(cfg))
            run_dir = rb.ROOT / "experiments" / "runs" / run_id
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "config.json").write_bytes(rb.canon(cfg))
            (run_dir / "env.json").write_bytes(rb.canon(env))
            for i in range(1, a.repeat + 1):
                rid = f"{run_id}_r{i}"
                base = {"run_id": rid, "config_id": a.config_id, "phase": "eval", "origin": "local",
                        "workload": f"code-task-{task}", "model_id": "M0", "model_sha256": "55983c5a75a1ab969824077b3bb3de4146e82a9234072b48ad4e8f92ad3fe9f1",
                        "engine_commit": env["engine_commit"], "settings_id": "S0", "ctx": a.ctx, "parallel": 1,
                        "kv": "int8", "mtp": "on", "thinking": "on", "cache_state": "warm" if i > 1 else "cold",
                        "git_commit": commit, "git_dirty": dirty, "config_sha256": config_sha, "env_sha256": env_sha}
                row, res = rb.measure(a.base_url, api_key, prompt, budget, a.timeout, server_cfg, base)
                if row.get("status") == "ok":
                    code = extract_code(res.get("answer", "")) if res.get("answer") else None
                    passed, summary = run_tests(task, code)
                    row["tests_passed"] = passed
                    row["note"] = f"{row['note']}; tests: {summary}"
                    (run_dir / f"answer_r{i}.md").write_text(res.get("answer", ""), encoding="utf-8")
                    (run_dir / f"reasoning_chars_r{i}.txt").write_text(str(len(res.get("reasoning", ""))), encoding="utf-8")
                rb.write_row(row)
                print(json.dumps({c: row.get(c) for c in ("run_id", "status", "input_tokens", "max_tokens", "output_tokens",
                                                          "finish_reason", "answer_reached", "tests_passed", "tg_tps",
                                                          "tt_reasoning_ms", "tt_answer_ms", "total_ms", "peak_vram_mb",
                                                          "peak_ram_mb", "experts_vram", "ssd_read_mb")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
