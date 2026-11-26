"""대화 캐시 A/B (T-013 원인 가설): 서버를 띄운 상태에서 한 조건을 잰다. 조건 간 서버 재시작은 cache-chain.ps1 이 한다.

잰 것: 후속 턴 재사용(probe_cache 변형 tools_all · reencode · reencode_reason, 각 2회), 생성 속도(256 토큰 1회),
메모리(남은 RAM · 커밋 여유 · 페이지 파일 · strata.exe 작업 집합 · private · 페이지 폴트), /metrics 의 파일 · 캐시 줄,
엔진 로그의 'conversation cache' 줄. 결과는 experiments/probes/cache_ab_<날짜>_<조건>.json.

    python scripts/bench/cache_ab.py --cond none|cm512|cm1024 --log <엔진 로그>
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

import probe_cache as pc

ROOT = Path(__file__).resolve().parents[2]
MEM_PS = ("$o = Get-CimInstance Win32_OperatingSystem; $p = Get-CimInstance Win32_Process -Filter \"Name='strata.exe'\" | Select-Object -First 1; "
          "$pf = Get-CimInstance Win32_PageFileUsage | Select-Object -First 1; "
          "[pscustomobject]@{free_ram_gb = [math]::Round($o.FreePhysicalMemory / 1MB, 3); commit_free_gb = [math]::Round($o.FreeVirtualMemory / 1MB, 3); "
          "pagefile_used_mb = $pf.CurrentUsage; strata_ws_gb = [math]::Round($p.WorkingSetSize / 1GB, 3); "
          "strata_private_gb = [math]::Round($p.PrivatePageCount / 1GB, 3); strata_page_faults = $p.PageFaults} | ConvertTo-Json -Compress")


def mem() -> dict:
    out = subprocess.run(["powershell", "-NoProfile", "-Command", MEM_PS], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
    try:
        return {"ts": time.strftime("%H:%M:%S"), **json.loads(out)}
    except json.JSONDecodeError:
        return {"ts": time.strftime("%H:%M:%S"), "error": out[-300:]}


def metrics(base: str, key: str) -> list[str]:
    try:
        req = urllib.request.Request(base + "/metrics", headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            txt = r.read().decode("utf-8", "replace")
    except Exception as ex:  # noqa: BLE001
        return [f"error {ex}"]
    return [ln for ln in txt.splitlines() if not ln.startswith("#") and any(k in ln.lower() for k in ("file", "cache", "conversation", "park"))][:80]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cond", required=True)
    ap.add_argument("--log", required=True, help="이 조건의 엔진 로그 (conversation cache 줄을 모은다)")
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--repeat", type=int, default=2)
    a = ap.parse_args()
    key = os.environ.get("STRATA_API_KEY", "strata-local")
    res = {"cond": a.cond, "date": time.strftime("%Y-%m-%d %H:%M:%S"), "mem": {"loaded": mem()}, "metrics": {"loaded": metrics(a.base_url, key)}}
    probes = []
    for r in range(a.repeat):
        for v in ("tools_all", "reencode", "reencode_reason"):
            recs = pc.run_variant(a.base_url, key, v)
            probes.append({"variant": v, "r": r + 1, "requests": recs})
            print(json.dumps({"cond": a.cond, "variant": v, "r": r + 1, "per_req": [(x["req"], x["prompt_tokens"], x["cached_tokens"],
                              x["prompt_n"], x["prompt_ms"]) for x in recs]}, ensure_ascii=False), flush=True)
    res["probes"] = probes
    res["mem"]["after_probe"] = mem()
    msgs = [{"role": "system", "content": f"[tg {time.time()}] 너는 코딩 도우미다."},
            {"role": "user", "content": "파이썬으로 이진 탐색 함수를 짧게 써라."}]
    rec, _ = pc.stream_req(a.base_url, key, msgs, None, 256)
    gen_ms = (rec["wall_ms"] or 0) - (rec["first_stream_ms"] or 0)
    rec["tg_tok_s"] = round(rec["completion_tokens"] / (gen_ms / 1000), 2) if rec.get("completion_tokens") and gen_ms > 0 else None
    res["tg"] = rec
    print(json.dumps({"cond": a.cond, "tg": rec["tg_tok_s"], "completion": rec["completion_tokens"]}), flush=True)
    res["mem"]["after_tg"] = mem()
    res["metrics"]["end"] = metrics(a.base_url, key)
    lp = Path(a.log)
    res["engine_log_cache_lines"] = ([ln for ln in lp.read_text(encoding="utf-8", errors="replace").splitlines()
                                      if "conversation" in ln.lower() or "prompt cache" in ln.lower()][-60:] if lp.exists() else ["(로그 없음)"])
    out = ROOT / "experiments" / "probes" / f"cache_ab_{time.strftime('%Y%m%d')}_{a.cond}.json"
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[cache_ab] wrote {out} | cache lines {len(res['engine_log_cache_lines'])}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
