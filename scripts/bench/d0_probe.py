r"""D0 결정성 탐침 (11-19 합의): seed 를 고정해도 회차마다 결과가 다른 원인을 가른다.

같은 요청(X3 dg_group_names navigate 첫 턴, H0 형식)을 조건을 바꿔 반복하고 출력(reasoning + content + tool_calls)을 비교한다.
  서버 A (기본, --mtp 2): R card-general x3 · R greedy x3 · P2 greedy (앞부분 재사용)
  서버 B (다시 띄움, --mtp 2): P2 greedy (처음부터) · R greedy · R card-general
  서버 C (--mtp 0): P2 greedy (처음부터) · R greedy x2 · R card-general
가르는 것: N5/N1 같은 서버 반복(A 안) · N2 재시작(A vs B) · N3 재사용 vs 처음부터(A P2 vs B P2) · N4 MTP(B vs C).
greedy = temperature 0 (나머지 키는 card-general 그대로). 결과: experiments/probes/d0_determinism_<날짜>.json. 원장 행은 쓰지 않는다.

    python d0_probe.py [--max-tokens 1024]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_x3 as x3  # noqa: E402

rb = x3.rb
ROOT = Path(r"C:\strata-lab")
SERVE = ROOT / "scripts" / "serve-ctx.ps1"
BASE = "http://127.0.0.1:8080"
SYS = ("너는 pypa/packaging 저장소(고정 커밋)에서 작업하는 코딩 에이전트다. 파일은 미리 주어지지 않는다. "
       "list_files · grep · read_file 도구로 필요한 코드를 찾아 읽고, edit_file 도구로 직접 고쳐라.")
TASK = "dg_group_names"
TOOL_RESULT = "(D0 탐침: 고정 도구 결과. 실제 실행 없음)"


def health() -> dict | None:
    try:
        with urllib.request.urlopen(BASE + "/health", timeout=3) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        return None


def serve(tag: str, extra: str = "") -> dict:
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SERVE), "-Stop"], capture_output=True)
    log = open(ROOT / "engine" / f"serve-d0-{tag}.log", "w", encoding="utf-8")
    args = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SERVE), "-Context", "32768", "-Tag", f"d0{tag}"]
    if extra:
        args += ["-ExtraArgs", extra]
    subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(180):
        time.sleep(5)
        h = health()
        if h and h.get("loaded") and h.get("max_context") == 32768:
            return h
    raise SystemExit(f"서버 {tag} 가 뜨지 않음")


def flat(data: dict) -> str:
    m = data["choices"][0]["message"]
    calls = [{"name": c["function"]["name"], "arguments": c["function"].get("arguments")} for c in (m.get("tool_calls") or [])]
    return json.dumps({"reasoning": m.get("reasoning_content") or "", "content": m.get("content") or "", "calls": calls},
                      ensure_ascii=False, sort_keys=True)


def first_diff(a: str, b: str) -> int | None:
    if a == b:
        return None
    n = min(len(a), len(b))
    return next((i for i in range(n) if a[i] != b[i]), n)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-tokens", type=int, default=1024)
    a = ap.parse_args()
    key = os.environ.get("STRATA_API_KEY", "strata-local")
    general = dict(x3.SAMPLING_SETS["card-general"])
    greedy = {**general, "temperature": 0.0}
    task_txt = (x3.TASKS / TASK / "prompt.md").read_text(encoding="utf-8")
    R = [{"role": "system", "content": SYS}, {"role": "user", "content": "### 과제\n" + task_txt + "\n\n" + x3.NAV_FORMAT}]
    out: list[dict] = []
    p2: list | None = None

    def ask(server: str, label: str, msgs: list, smp: dict) -> str:
        rb.SAMPLING.clear()
        rb.SAMPLING.update(smp)
        data, ms = x3.chat_once(BASE, key, msgs, a.max_tokens, 1800, x3.NAV_TOOLS)
        s = flat(data)
        tm = data.get("timings") or {}
        u = data.get("usage") or {}
        rec = {"server": server, "label": label, "temperature": smp["temperature"], "n_msgs": len(msgs), "chars": len(s),
               "sha256": rb.sha256_bytes(s.encode("utf-8")), "completion_tokens": u.get("completion_tokens"),
               "prompt_tokens": u.get("prompt_tokens"), "cache_n": tm.get("cache_n"), "prompt_n": tm.get("prompt_n"),
               "finish": data["choices"][0].get("finish_reason"), "wall_ms": round(ms, 1), "text": s}
        out.append(rec)
        print(json.dumps({k: v for k, v in rec.items() if k != "text"}, ensure_ascii=False), flush=True)
        return s

    def build_p2(first: str, data_msgs: list) -> list:
        f = json.loads(first)
        m = {"role": "assistant", "content": f["content"], "reasoning_content": f["reasoning"]}
        msgs = list(data_msgs)
        if f["calls"]:
            m["tool_calls"] = [{"id": f"d0_{i}", "type": "function", "function": {"name": c["name"], "arguments": c["arguments"] or "{}"}}
                               for i, c in enumerate(f["calls"])]
            msgs.append(m)
            msgs += [{"role": "tool", "tool_call_id": f"d0_{i}", "content": TOOL_RESULT} for i in range(len(f["calls"]))]
        else:
            msgs.append(m)
            msgs.append({"role": "user", "content": "계속하라."})
        return msgs

    t0 = time.time()
    serve("A")
    for i in range(3):
        ask("A", f"R_general_{i + 1}", R, general)
    g1 = ask("A", "R_greedy_1", R, greedy)
    for i in range(1, 3):
        ask("A", f"R_greedy_{i + 1}", R, greedy)
    p2 = build_p2(g1, R)
    ask("A", "R_greedy_setup", R, greedy)             # 서버가 R + 그 출력을 들고 있게 한다(재사용 조건, 출력이 g1 과 같을 때만)
    ask("A", "P2_greedy_reuse", p2, greedy)
    serve("B")
    ask("B", "P2_greedy_cold", p2, greedy)
    ask("B", "R_greedy_1", R, greedy)
    ask("B", "R_general_1", R, general)
    serve("C", "--mtp 0")
    ask("C", "P2_greedy_cold", p2, greedy)
    ask("C", "R_greedy_1", R, greedy)
    ask("C", "R_greedy_2", R, greedy)
    ask("C", "R_general_1", R, general)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SERVE), "-Stop"], capture_output=True)

    by = {(r["server"], r["label"]): r["text"] for r in out}
    pairs = {
        "N5 같은 서버 general 반복 (A1 vs A2)": (("A", "R_general_1"), ("A", "R_general_2")),
        "N5 같은 서버 general 반복 (A1 vs A3)": (("A", "R_general_1"), ("A", "R_general_3")),
        "N5 같은 서버 greedy 반복 (A1 vs A2)": (("A", "R_greedy_1"), ("A", "R_greedy_2")),
        "N5 같은 서버 greedy 반복 (A1 vs A3)": (("A", "R_greedy_1"), ("A", "R_greedy_3")),
        "N2 재시작 greedy (A vs B)": (("A", "R_greedy_1"), ("B", "R_greedy_1")),
        "N2 재시작 general (A vs B)": (("A", "R_general_1"), ("B", "R_general_1")),
        "N3 재사용 vs 처음부터 (A reuse vs B cold)": (("A", "P2_greedy_reuse"), ("B", "P2_greedy_cold")),
        "N4 MTP 2 vs 0 greedy (B vs C)": (("B", "R_greedy_1"), ("C", "R_greedy_1")),
        "N4 MTP 2 vs 0 P2 cold (B vs C)": (("B", "P2_greedy_cold"), ("C", "P2_greedy_cold")),
        "MTP 0 같은 서버 greedy 반복 (C1 vs C2)": (("C", "R_greedy_1"), ("C", "R_greedy_2")),
    }
    verdict = {}
    for name, (x, y) in pairs.items():
        d = first_diff(by[x], by[y])
        verdict[name] = {"same": d is None, "first_diff_char": d, "chars": [len(by[x]), len(by[y])]}
        print(f"{'같음 ' if d is None else '다름 '} {name}" + ("" if d is None else f"  (첫 차이 {d}자)"), flush=True)
    day = dt.date.today().strftime("%Y%m%d")
    dst = ROOT / "experiments" / "probes" / f"d0_determinism_{day}.json"
    dst.write_text(json.dumps({"probe": "D0", "task": TASK, "max_tokens": a.max_tokens, "general": general, "greedy": greedy,
                               "minutes": round((time.time() - t0) / 60, 1), "verdict": verdict, "requests": out},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", dst, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
