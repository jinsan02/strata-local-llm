"""후속 턴에서 무엇을 다시 읽는지: 같은 세션 요청별 prompt / cached / 새로 읽은 토큰 / 첫 스트림.

변수는 한 번에 하나. 각 변형은 시스템 지시 맨 앞의 고유 nonce 로 다른 변형과 캐시를 나누지 않는다(세션 첫 요청 = cold).
  A tools_all       : 4요청 모두 도구 목록 포함 (기준)
  B final_no_tools  : A 와 같고 마지막 요청만 도구 목록을 뺀다 (러너의 force 턴과 같은 동작)
  C reencode        : 1요청은 모델이 실제로 생성(thinking + 도구 호출), 2요청에 그 답을 reasoning 없이 다시 보냄
  D reencode_reason : C 와 같고 2요청에 reasoning_content 를 함께 보냄
  E volatile_env    : A 와 같고 시스템 지시 끝의 '작업 폴더 정보'(시각 포함)가 요청마다 바뀜
서버가 값을 안 주면 None(NA) 으로 남긴다. 0 은 실측 0 이다.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
import uuid
from pathlib import Path

SRC = Path(r"C:\strata-lab\work\packaging-src")
FILES = ["src/packaging/version.py", "src/packaging/specifiers.py"]
TOOLS = [{"type": "function", "function": {"name": "read_file", "description": "파일을 줄 번호와 함께 읽기",
          "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
         {"type": "function", "function": {"name": "grep", "description": "정규식 검색",
          "parameters": {"type": "object", "properties": {"pattern": {"type": "string"}}, "required": ["pattern"]}}}]
SYS = "너는 pypa/packaging 저장소에서 작업하는 코딩 에이전트다. 도구로 코드를 읽고 고쳐라."
TASK = "Version 클래스에 새 메서드를 추가해야 한다. 먼저 관련 파일을 읽어라."


def stream_req(base, key, msgs, tools, max_tokens):
    body = {"model": "strata", "messages": msgs, "max_tokens": max_tokens, "stream": True,
            "stream_options": {"include_usage": True}, "temperature": 0.6, "top_p": 0.95}
    if tools:
        body["tools"] = tools
    req = urllib.request.Request(base.rstrip("/") + "/v1/chat/completions", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    t0 = time.perf_counter()
    first, usage, timings, text, reasoning, calls = None, None, None, "", "", {}
    with urllib.request.urlopen(req, timeout=900) as r:
        for raw in r:
            line = raw.decode("utf-8").strip()
            if not line.startswith("data:") or line[5:].strip() == "[DONE]":
                continue
            e = json.loads(line[5:])
            usage = e.get("usage") or usage
            timings = e.get("timings") or timings
            for ch in e.get("choices") or []:
                d = ch.get("delta") or {}
                if first is None and (d.get("content") or d.get("reasoning_content") or d.get("tool_calls")):
                    first = (time.perf_counter() - t0) * 1000
                text += d.get("content") or ""
                reasoning += d.get("reasoning_content") or ""
                for tc in d.get("tool_calls") or []:
                    c = calls.setdefault(tc.get("index", 0), {"id": None, "name": None, "args": ""})
                    c["id"] = tc.get("id") or c["id"]
                    fn = tc.get("function") or {}
                    c["name"] = fn.get("name") or c["name"]
                    c["args"] += fn.get("arguments") or ""
    u = usage or {}
    tm = timings or {}
    rec = {"prompt_tokens": u.get("prompt_tokens"), "cached_tokens": (u.get("prompt_tokens_details") or {}).get("cached_tokens"),
           "cache_n": tm.get("cache_n"), "prompt_n": tm.get("prompt_n"), "prompt_ms": tm.get("prompt_ms"),
           "first_stream_ms": None if first is None else round(first, 1), "wall_ms": round((time.perf_counter() - t0) * 1000, 1),
           "completion_tokens": u.get("completion_tokens"), "tools": bool(tools)}
    return rec, {"text": text, "reasoning": reasoning, "calls": list(calls.values())}


def file_out(rel):
    lines = (SRC / rel).read_text(encoding="utf-8").splitlines()
    return "\n".join(f"{i:5d}  {ln}" for i, ln in enumerate(lines[:400], 1))[:12000]


def synth_turn(i, rel):
    cid = f"call_{i}"
    return [{"role": "assistant", "content": "", "tool_calls": [{"id": cid, "type": "function",
             "function": {"name": "read_file", "arguments": json.dumps({"path": rel})}}]},
            {"role": "tool", "tool_call_id": cid, "content": file_out(rel)}]


def run_variant(base, key, name):
    nonce = uuid.uuid4().hex[:12]
    sys_txt = lambda k: f"[session {nonce}] {SYS}" + (f"\n작업 폴더: C:/work/{nonce} · 시각 {time.strftime('%H:%M:%S')}.{k}" if name == "volatile_env" else "")  # noqa: E731
    recs = []
    msgs = [{"role": "system", "content": sys_txt(0)}, {"role": "user", "content": TASK}]
    if name in ("reencode", "reencode_reason"):
        rec, out = stream_req(base, key, msgs, TOOLS, 1536)
        recs.append({"req": 1, **rec, "generated": True})
        c = out["calls"][0] if out["calls"] else {"id": "call_g", "name": "read_file", "args": json.dumps({"path": FILES[0]})}
        am = {"role": "assistant", "content": out["text"], "tool_calls": [{"id": c["id"] or "call_g", "type": "function",
              "function": {"name": c["name"] or "read_file", "arguments": c["args"] or "{}"}}]}
        if name == "reencode_reason":
            am["reasoning_content"] = out["reasoning"]
        msgs += [am, {"role": "tool", "tool_call_id": am["tool_calls"][0]["id"], "content": file_out(FILES[0])}]
        rec, _ = stream_req(base, key, msgs, TOOLS, 1)
        recs.append({"req": 2, **rec, "prev_prompt": recs[0]["prompt_tokens"], "reasoning_chars": len(out["reasoning"])})
        return recs
    for k in range(4):
        if k == 1:
            msgs += synth_turn(1, FILES[0])
        elif k == 2:
            msgs += synth_turn(2, FILES[1])
        elif k == 3:
            msgs.append({"role": "user", "content": "이제 도구를 더 쓸 수 없다. 바꾼 내용을 짧게 답하라."})
        if name == "volatile_env":
            msgs[0] = {"role": "system", "content": sys_txt(k)}
        tools = None if (name == "final_no_tools" and k == 3) else TOOLS
        rec, _ = stream_req(base, key, msgs, tools, 1)
        recs.append({"req": k + 1, **rec})
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--variants", nargs="+", default=["tools_all", "final_no_tools", "reencode", "reencode_reason", "volatile_env"])
    ap.add_argument("--repeat", type=int, default=2)
    ap.add_argument("--out", default="probe_cache.json")
    a = ap.parse_args()
    key = os.environ.get("STRATA_API_KEY", "strata-local")
    res = []
    for r in range(a.repeat):
        for v in a.variants:
            recs = run_variant(a.base_url, key, v)
            res.append({"variant": v, "r": r + 1, "requests": recs})
            print(json.dumps({"variant": v, "r": r + 1, "per_req": [(x["req"], x["prompt_tokens"], x["cached_tokens"], x["prompt_n"],
                              x["first_stream_ms"]) for x in recs]}, ensure_ascii=False), flush=True)
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
