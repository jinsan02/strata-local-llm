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


PAD_SOURCES = [Path(r"C:\strata-lab\engine\strata_cli"), Path(r"C:\strata-lab\engine\strata_control")]


def pad_files(chars: int) -> str:
    """실제 코드 파일을 파일 머리표와 함께 이어 붙여 약 chars 글자의 '관련 파일 여러 개' 를 만든다 (결정적 순서)."""
    parts, n = [], 0
    files = sorted(p for d in PAD_SOURCES if d.exists() for p in d.rglob("*.py"))
    for p in files:
        if n >= chars:
            break
        body = p.read_text(encoding="utf-8", errors="replace")
        rel = p.relative_to(Path(r"C:\strata-lab\engine")).as_posix()
        chunk = f"### FILE: {rel}\n```python\n{body}\n```\n\n"
        parts.append(chunk[: max(0, chars - n)] if n + len(chunk) > chars else chunk)
        n += len(parts[-1])
    return "".join(parts)


def build_long_prompt(task_prompt: str, pad_chars: int, position: str) -> str:
    """코딩 세션처럼: 저장소 파일 여러 개 + 과제. position=end 는 과제가 마지막, middle 은 파일 사이."""
    if pad_chars <= 0:
        return task_prompt
    pad = pad_files(pad_chars)
    head = "다음은 작업 중인 저장소의 파일들이다. 파일 목록 뒤(또는 사이)에 있는 과제만 수행하라.\n\n"
    task = f"### 과제\n{task_prompt}\n\n"
    if position == "middle":
        half = len(pad) // 2
        cut = pad.rfind("### FILE:", 0, half) if pad.rfind("### FILE:", 0, half) > 0 else half
        return head + pad[:cut] + task + pad[cut:] + "\n위 과제를 수행하라. 다른 파일은 고치지 마라."
    return head + pad + task


def extract_code(answer: str) -> str | None:
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", answer, flags=re.S)
    return blocks[-1] if blocks else None


def count_tests(tests: Path) -> int | None:
    """테스트 파일의 전체 테스트 수. solution 의 이름을 None 으로 둔 가짜 모듈로 수집만 한다.

    코드 블록이 없을 때 그냥 수집하면 import 오류 1건이 '1개' 로 세어졌다 (2026-11-18 xb lru_cache b2k: 0/1, 실제 5개).
    """
    names = re.findall(r"^from solution import (.+)$", tests.read_text(encoding="utf-8"), flags=re.M)
    stub = "".join(f"{n.strip()} = None\n" for line in names for n in line.split(","))
    with tempfile.TemporaryDirectory() as d:
        shutil.copy(tests, d)
        Path(d, "solution.py").write_text(stub, encoding="utf-8")
        r = subprocess.run([PY, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", d],
                           capture_output=True, text=True, timeout=120, cwd=d)
        m = re.search(r"(\d+) tests? collected", r.stdout) or re.search(r"^(\d+) tests?", r.stdout, flags=re.M)
        if m:
            return int(m.group(1))
        n = len([ln for ln in r.stdout.splitlines() if "::" in ln])
        return n or None


def run_tests(task: str, code: str | None) -> tuple[str, str]:
    """(통과/전체, 요약). 코드가 없으면 0/전체."""
    tests = TASKS / task / "test_solution.py"
    total = None
    with tempfile.TemporaryDirectory() as d:
        shutil.copy(tests, d)
        if code is None:
            n = count_tests(tests)
            return (f"0/{n}" if n else "0/NA"), "코드 블록 없음"
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
        n = count_tests(tests)
        if n and total < n:
            # 답 코드에 문법 오류가 있으면 수집 오류 1건이 '전체 1개' 로 세어졌다 (xb2 merge_intervals b4k r2: 0/1, 실제 6개)
            total = n
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
    ap.add_argument("--input-tokens", type=int, default=0,
                    help="X2: 저장소 파일을 붙여 실제 입력(템플릿 포함)을 이 토큰 수 근처로 만든다. 0 이면 과제만")
    ap.add_argument("--position", choices=["end", "middle"], default="end")
    ap.add_argument("--chars-per-token", type=float, default=3.0)
    ap.add_argument("--workload", default=None)
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
        task_prompt = (TASKS / task / "prompt.md").read_text(encoding="utf-8")
        tests_sha = rb.sha256_bytes((TASKS / task / "test_solution.py").read_bytes())
        prompt = task_prompt
        exact = (rb.stream_chat(a.base_url, api_key, prompt, 1, a.timeout).get("usage") or {}).get("prompt_tokens")
        if a.input_tokens > 0:
            # 문자/토큰 비를 한 번 재서 맞춘다 (서버 보고 prompt_tokens 기준, 템플릿 포함)
            cpt = a.chars_per_token
            for _ in range(3):
                prompt = build_long_prompt(task_prompt, int((a.input_tokens - (exact or 0)) * cpt), a.position)
                got = (rb.stream_chat(a.base_url, api_key, prompt, 1, a.timeout).get("usage") or {}).get("prompt_tokens")
                if not got or abs(got - a.input_tokens) <= max(64, a.input_tokens // 100):
                    break
                cpt *= (a.input_tokens - (exact or 0)) / max(1, got - (exact or 0))
            exact = got
        for budget in a.budgets:
            if exact is not None and exact + budget > a.ctx:
                print(json.dumps({"task": task, "budget": budget, "skip": f"입력 {exact} + 예산 {budget} > ctx {a.ctx}"},
                                 ensure_ascii=False))
                continue
            inp = f"_in{round(a.input_tokens / 1024)}k{'m' if a.position == 'middle' else ''}" if a.input_tokens else ""
            run_id = f"{a.prefix}_m0_e0_s0_ctx{k}k{inp}_{task}_b{budget // 1024}k"
            cfg = {"task": task, "prompt_sha256": rb.sha256_bytes(prompt.encode("utf-8")), "tests_sha256": tests_sha,
                   "budget": budget, "ctx": a.ctx, "sampling": rb.SAMPLING, "server_config": server_cfg,
                   "prompt_tokens_exact": exact, "input_tokens_target": a.input_tokens, "position": a.position,
                   "pad_sources": [str(p) for p in PAD_SOURCES] if a.input_tokens else []}
            config_sha = rb.sha256_bytes(rb.canon(cfg))
            run_dir = rb.ROOT / "experiments" / "runs" / run_id
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "config.json").write_bytes(rb.canon(cfg))
            (run_dir / "env.json").write_bytes(rb.canon(env))
            for i in range(1, a.repeat + 1):
                rid = f"{run_id}_r{i}"
                base = {"run_id": rid, "config_id": a.config_id, "phase": "eval", "origin": "local",
                        "workload": a.workload or (f"code-files-{task}" if a.input_tokens else f"code-task-{task}"), "model_id": "M0", "model_sha256": "55983c5a75a1ab969824077b3bb3de4146e82a9234072b48ad4e8f92ad3fe9f1",
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
