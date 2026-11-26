"""측정 러너 — 변경안 v2.1 7절 지표를 원장(experiments/LEDGER.tsv)에 쓴다.

본체에서 conda 환경 strata_local_llm 으로 돈다 (표준 라이브러리 + psutil).

    python scripts/bench/run_bench.py --run-id x0_m0_e0_s0_ctx8k --config-id X0 --phase bench \
        --ctx 8192 --workload fixed-512 --target-tokens 512 --max-tokens 128 --repeat 3

- 스트리밍으로 첫 스트림(reasoning 또는 content) 지연, 첫 최종 답변 지연, 완료 시간을 잰다
- 토큰 수·속도는 엔진 보고값(usage, timings)만 쓴다. SSE 조각·문자 수로 계산하지 않는다 (RULES 6)
- Peak VRAM 은 nvidia-smi 500ms 간격 관측값, RAM·디스크 읽기는 엔진 프로세스(strata.exe) 기준
- 반복마다 한 행. run_id 에 _r<n> 을 붙인다. 실패도 status=fail 로 남긴다 (RULES 5)
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.validate_ledger import COLUMNS  # noqa: E402

LEDGER = ROOT / "experiments" / "LEDGER.tsv"
SOURCE_TEXT = ROOT / "docs" / "plan-v2.0.md"          # 고정 문항의 재료 (저장소 안, 바뀌면 해시가 바뀐다)
# 서버가 qwen35moe(Qwen3.6) thinking 에 쓰는 권장 샘플링과 같은 값을 명시해 고정한다
# (serve/server.py 의 qwen35moe thinking 세트, 변경안 5절). 2026-11-18 X0 8K 첫 3행은 0.6/0.95/20 이었다.
SAMPLING = {"temperature": 1.0, "top_p": 0.95, "top_k": 20, "presence_penalty": 1.5, "seed": 42}
# 요청 본문에 더할 서버 옵션 (예: B1 의 reasoning_budget_tokens). 러너가 채운다.
EXTRA_BODY: dict = {}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def git(*args) -> str:
    out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return out.stdout.strip()


# 2026-11-19 부터 원장 git_dirty 의 뜻: 측정 결과에 영향을 주는 경로(코드 · 설정 · 과제)만 본다.
# 그전에는 작업 트리 전체였고, 측정 중 원장 · env 로그가 늘 바뀌어 거의 모든 행이 1 이었다 (LEDGER_SCHEMA 정정 기록).
DIRTY_PATHS = ("scripts", "configs", "tools", "pyproject.toml", "AGENTS.md")


def code_dirty() -> str:
    return "1" if git("status", "--porcelain", "--", *DIRTY_PATHS) else "0"


# ── 관측 ──────────────────────────────────────────────────────────────────
class Sampler(threading.Thread):
    """500ms 마다 GPU 사용 메모리와 엔진 프로세스 RAM 을 본다. 최대값은 관측 피크다."""

    def __init__(self, interval=0.5):
        super().__init__(daemon=True)
        self.interval, self.stop_ev = interval, threading.Event()
        self.peak_vram = 0
        self.peak_ram = 0
        self.proc = find_engine()

    def run(self):
        while not self.stop_ev.is_set():
            try:
                v = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                   capture_output=True, text=True, timeout=5, encoding="utf-8", errors="replace").stdout.split()
                if v:
                    self.peak_vram = max(self.peak_vram, int(v[0]))
            except Exception:
                pass
            if self.proc is not None:
                try:
                    self.peak_ram = max(self.peak_ram, self.proc.memory_info().rss // (1024 * 1024))
                except Exception:
                    self.proc = None
            self.stop_ev.wait(self.interval)


def find_engine():
    try:
        import psutil
    except ImportError:
        return None
    for p in psutil.process_iter(["name"]):
        if (p.info.get("name") or "").lower() == "strata.exe":
            return p
    return None


def read_bytes(proc) -> int | None:
    try:
        return proc.io_counters().read_bytes
    except Exception:
        return None


# ── 문항 ──────────────────────────────────────────────────────────────────
def build_prompt(target_tokens: int, chars_per_token: float) -> str:
    text = SOURCE_TEXT.read_text(encoding="utf-8")
    need = int(target_tokens * chars_per_token)
    body = (text * (need // max(len(text), 1) + 1))[:need]
    return ("아래 문서를 읽고 마지막 줄의 질문에 한국어로 답하라.\n\n" + body +
            "\n\n질문: 이 문서의 핵심 목적을 세 문장으로 요약하라.")


# ── 요청 ──────────────────────────────────────────────────────────────────
def stream_chat(base_url: str, api_key: str, prompt, max_tokens: int, timeout: float) -> dict:
    """prompt: 문자열(사용자 메시지 하나) 또는 messages 리스트."""
    messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
    body = {"model": "strata", "stream": True, "stream_options": {"include_usage": True},
            "max_tokens": max_tokens, "messages": messages, **SAMPLING, **EXTRA_BODY}
    req = urllib.request.Request(base_url.rstrip("/") + "/v1/chat/completions", data=canon(body), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
    t0 = time.perf_counter()
    first_stream = first_answer = first_reason = None
    usage = timings = finish = None
    extra = {}
    answer, reasoning = [], []
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            ev = json.loads(data)
            now = time.perf_counter()
            for ch in ev.get("choices") or []:
                d = ch.get("delta") or {}
                if (d.get("reasoning_content") or d.get("content")) and first_stream is None:
                    first_stream = now
                if d.get("reasoning_content"):
                    reasoning.append(d["reasoning_content"])
                    if first_reason is None:
                        first_reason = now
                if d.get("content"):
                    answer.append(d["content"])
                    if first_answer is None and "".join(answer).strip():
                        first_answer = now
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
            usage = ev.get("usage") or usage
            timings = ev.get("timings") or timings
            for k in ("reasoning_tokens", "strata"):
                if k in ev:
                    extra[k] = ev[k]
    t1 = time.perf_counter()
    ms = lambda t: round((t - t0) * 1000, 1) if t is not None else None  # noqa: E731
    return {"ttft_ms": ms(first_stream), "tt_reasoning_ms": ms(first_reason), "tt_answer_ms": ms(first_answer),
            "total_ms": ms(t1), "usage": usage, "timings": timings, "finish": finish, "extra": extra,
            "answer": "".join(answer), "reasoning": "".join(reasoning)}


def experts_vram(server_cfg: dict) -> str | None:
    """엔진 로그의 마지막 'hybrid experts: N of 256 per layer in VRAM' — 이 서버 기동 때의 expert 캐시 상태."""
    log = server_cfg.get("log")
    try:
        text = Path(log).read_text(encoding="utf-8", errors="replace") if log else ""
    except OSError:
        return None
    import re
    hits = re.findall(r"hybrid experts: (\d+) of (\d+) per layer in VRAM", text)
    return f"{hits[-1][0]}/{hits[-1][1]}" if hits else None


def check_budget(input_tokens, max_tokens: int, ctx: int):
    """입력(템플릿 포함) + 출력·reasoning 예산이 컨텍스트를 넘으면 실행하지 않는다 (사용자 지시 4)."""
    if input_tokens is not None and input_tokens + max_tokens > ctx:
        raise SystemExit(f"예산 초과: 입력 {input_tokens} + 출력 예산 {max_tokens} = {input_tokens + max_tokens} > ctx {ctx}")


def engine_drafts(server_cfg: dict):
    """엔진 로그의 마지막 요청 줄 'drafts accepted A of O' -> (A, O).

    서버 /metrics 의 drafts_* 는 v0.2.15 qwen36 경로에서 엔진이 158/198 을 보고해도 0/0 으로 남는다
    (2026-11-18 확인, STATE Q10). 그래서 엔진 로그를 출처로 쓴다.
    """
    import re
    log = server_cfg.get("log")
    try:
        with open(log, "rb") as f:
            f.seek(0, 2); f.seek(max(0, f.tell() - 65536))
            tail = f.read().decode("utf-8", "replace")
    except (OSError, TypeError):
        return None
    hits = re.findall(r"strata serve: session \d+: .*drafts accepted (\d+) of (\d+)", tail)
    return (int(hits[-1][0]), int(hits[-1][1])) if hits else None


def draft_cols(server_cfg: dict) -> dict:
    """시도 0 은 '초안 시도 미기록' — NA 로 남기고 note 에 쓴다 (사용자 지시 3)."""
    d = engine_drafts(server_cfg)
    if d is None:
        return {"drafts_offered": None, "drafts_accepted": None, "_draft_note": "MTP 초안: 엔진 로그 없음"}
    acc, off = d
    if off == 0:
        return {"drafts_offered": None, "drafts_accepted": None,
                "_draft_note": "MTP 초안 시도 미기록 (q36 경로는 logits 가 필요 없는 greedy 단독 요청만 초안)"}
    return {"drafts_offered": off, "drafts_accepted": acc, "_draft_note": f"MTP 수락률 {acc / off:.0%}"}


def reasoning_tokens(res: dict):
    u = res.get("usage") or {}
    det = u.get("completion_tokens_details") or {}
    for v in (det.get("reasoning_tokens"), (res.get("extra") or {}).get("reasoning_tokens"), u.get("reasoning_tokens")):
        if v is not None:
            return v
    return None


def last_request_metrics(base_url: str, api_key: str) -> dict:
    """서버 /metrics 의 마지막 요청 기록: file_mb(SSD 에서 읽은 expert), drafts(MTP), hit_rate, pcie_share."""
    try:
        req = urllib.request.Request(base_url.rstrip("/") + "/metrics", headers={"Authorization": f"Bearer {api_key}"})
        with urllib.request.urlopen(req, timeout=15) as r:
            reqs = json.loads(r.read().decode("utf-8")).get("requests") or []
        return reqs[-1] if reqs else {}
    except Exception:
        return {}


def measure(base_url, api_key, prompt, max_tokens, timeout, server_cfg, base_row, note="", extra_cols=None):
    """요청 하나를 재고 원장 행을 만든다. run_bench(고정 문항)와 run_coding(코딩 과제)이 같이 쓴다."""
    sampler = Sampler()
    rb0 = read_bytes(sampler.proc) if sampler.proc else None
    sampler.start()
    row = {"ts_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "max_tokens": max_tokens,
           "experts_vram": experts_vram(server_cfg), **base_row}
    try:
        res = stream_chat(base_url, api_key, prompt, max_tokens, timeout)
        sampler.stop_ev.set(); sampler.join(2)
        u, tm = res.get("usage") or {}, res.get("timings") or {}
        rb1 = read_bytes(sampler.proc) if sampler.proc else None
        mreq = last_request_metrics(base_url, api_key)
        res["server_request"] = mreq
        dc = draft_cols(server_cfg)
        srv = (f"file_mb {mreq.get('file_mb')}; hit_rate {mreq.get('hit_rate')}; pcie_share {mreq.get('pcie_share')}; "
               f"cached {((u.get('prompt_tokens_details') or {}).get('cached_tokens'))}") if mreq else "metrics 없음"
        row.update(status="ok", input_tokens=u.get("prompt_tokens"), output_tokens=u.get("completion_tokens"),
                   reasoning_tokens=reasoning_tokens(res), finish_reason=res["finish"],
                   answer_reached=1 if res["answer"].strip() else 0,
                   pp_tps=round(tm["prompt_per_second"], 2) if tm.get("prompt_per_second") else None,
                   tg_tps=round(tm["predicted_per_second"], 2) if tm.get("predicted_per_second") else None,
                   ttft_ms=res["ttft_ms"], tt_reasoning_ms=res["tt_reasoning_ms"], tt_answer_ms=res["tt_answer_ms"],
                   total_ms=res["total_ms"], peak_vram_mb=sampler.peak_vram or None, peak_ram_mb=sampler.peak_ram or None,
                   # SSD 의존도: 엔진이 보고한 file_mb(파일에서 읽은 expert), 없으면 프로세스 읽기량
                   ssd_read_mb=mreq.get("file_mb") if mreq.get("file_mb") is not None else (
                       round((rb1 - rb0) / 1048576, 1) if rb0 is not None and rb1 is not None else None),
                   drafts_offered=dc["drafts_offered"], drafts_accepted=dc["drafts_accepted"],
                   note="; ".join(x for x in (dc["_draft_note"], srv, "reasoning_tokens: chat API 미보고",
                                              "vram=500ms 관측 피크", note) if x))
        row.update(extra_cols or {})
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 - 실패도 기록한다
        sampler.stop_ev.set()
        row.update(status="fail", note=f"{type(e).__name__}: {e}"[:300])
        res = {"error": row["note"], "answer": "", "reasoning": ""}
    return row, res


def write_row(row: dict):
    line = "\t".join(str(row.get(c, "NA")) if row.get(c) not in (None, "") else "NA" for c in COLUMNS)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(line.replace("\r", " ") + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--config-id", required=True)
    ap.add_argument("--phase", default="bench")
    ap.add_argument("--origin", default="local")
    ap.add_argument("--workload", required=True)
    ap.add_argument("--target-tokens", type=int, required=True)
    ap.add_argument("--max-tokens", type=int, default=128)
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--warmup", type=int, default=1)
    ap.add_argument("--ctx", type=int, required=True)
    ap.add_argument("--parallel", type=int, default=1)
    ap.add_argument("--kv", default="fp32")  # q36 경로는 K·V FP32 (+prompt attention FP16 사본), --kv 미적용 (T-009)
    ap.add_argument("--mtp", default="on")
    ap.add_argument("--thinking", default="on")
    ap.add_argument("--model-id", default="M0")
    ap.add_argument("--model-sha256", default="55983c5a75a1ab969824077b3bb3de4146e82a9234072b48ad4e8f92ad3fe9f1")
    ap.add_argument("--settings-id", default="S0")
    ap.add_argument("--server-config", default=None,
                    help="기본: engine/strata-qwen36-ctx<ctx>.json (serve-ctx.ps1 이 만든 것), 없으면 setup 원본")
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--api-key-env", default="STRATA_API_KEY")
    ap.add_argument("--chars-per-token", type=float, default=2.2)
    ap.add_argument("--timeout", type=float, default=900)
    ap.add_argument("--note", default="")
    a = ap.parse_args()

    api_key = os.environ.get(a.api_key_env, "strata-local")
    engine_dir = Path(r"C:\strata-lab\engine")
    if a.server_config is None:
        cand = engine_dir / f"strata-qwen36-ctx{a.ctx}.json"
        a.server_config = str(cand if cand.exists() else engine_dir / "strata-qwen36-ud-q4_k_xl.json")
    server_cfg = json.loads(Path(a.server_config).read_text(encoding="utf-8")) if Path(a.server_config).exists() else {}
    cfg = {"args": {k: v for k, v in vars(a).items() if k not in ("note",)}, "sampling": SAMPLING,
           "server_config": server_cfg, "source_text": str(SOURCE_TEXT.relative_to(ROOT)),
           "source_text_sha256": sha256_bytes(SOURCE_TEXT.read_bytes())}
    env = {"engine_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=engine_dir, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip(),
           "engine_exe_sha256": sha256_bytes(Path(server_cfg["exe"]).read_bytes()) if server_cfg.get("exe") else None,
           "driver": subprocess.run(["nvidia-smi", "--query-gpu=driver_version,name", "--format=csv,noheader"],
                                    capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip(),
           "python": sys.version.split()[0]}
    config_sha, env_sha = sha256_bytes(canon(cfg)), sha256_bytes(canon(env))
    commit, dirty = git("rev-parse", "HEAD"), code_dirty()

    # 문항 길이 보정: 한 번 max_tokens=1 로 보내 실제 prompt_tokens 를 보고 문자/토큰 비를 맞춘다
    probe = build_prompt(a.target_tokens, a.chars_per_token)
    r0 = stream_chat(a.base_url, api_key, probe, 1, a.timeout)
    pt = (r0.get("usage") or {}).get("prompt_tokens")
    cpt = a.chars_per_token * (a.target_tokens / pt) if pt else a.chars_per_token
    prompt = build_prompt(a.target_tokens, cpt)
    exact = (stream_chat(a.base_url, api_key, prompt, 1, a.timeout).get("usage") or {}).get("prompt_tokens")
    check_budget(exact, a.max_tokens, a.ctx)
    cfg["prompt_sha256"] = sha256_bytes(prompt.encode("utf-8"))
    cfg["prompt_tokens_exact"] = exact
    config_sha = sha256_bytes(canon(cfg))

    run_dir = ROOT / "experiments" / "runs" / a.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_bytes(canon(cfg))
    (run_dir / "env.json").write_bytes(canon(env))

    for _ in range(a.warmup):
        stream_chat(a.base_url, api_key, prompt, a.max_tokens, a.timeout)

    base = {"config_id": a.config_id, "phase": a.phase, "origin": a.origin, "workload": a.workload,
            "model_id": a.model_id, "model_sha256": a.model_sha256, "engine_commit": env["engine_commit"],
            "settings_id": a.settings_id, "ctx": a.ctx, "parallel": a.parallel, "kv": a.kv, "mtp": a.mtp,
            "thinking": a.thinking, "git_commit": commit, "git_dirty": dirty, "config_sha256": config_sha,
            "env_sha256": env_sha}
    results = []
    for i in range(1, a.repeat + 1):
        rid = f"{a.run_id}_r{i}"
        row, res = measure(a.base_url, api_key, prompt, a.max_tokens, a.timeout, server_cfg,
                           {**base, "run_id": rid, "cache_state": "warm" if (a.warmup or i > 1) else "cold"}, a.note)
        results.append({"run_id": rid, **res})
        write_row(row)
        print(json.dumps({k: row.get(k) for k in ("run_id", "status", "input_tokens", "output_tokens", "reasoning_tokens",
                                                  "pp_tps", "tg_tps", "ttft_ms", "tt_answer_ms", "total_ms",
                                                  "peak_vram_mb", "peak_ram_mb", "ssd_read_mb")}, ensure_ascii=False))
    (run_dir / "summary.json").write_bytes(canon({"results": results}))
    return 0 if all("error" not in r for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
