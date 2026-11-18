"""도구 호출 한 바퀴 점검: 짧은 텍스트 -> 도구 호출 -> 같은 ID 의 도구 결과 -> 후속 응답.

세 API(Chat Completions = X3 러너, Anthropic Messages = Claude Code, OpenAI Responses = Codex) x (비스트림, 스트림).
스트림은 인자 조각을 이어 붙여 JSON 으로 읽히는지 본다. 실패는 단계로 나눈다:
  api      HTTP 오류 · 응답 모양이 규격과 다름 · 스트림 조각 조립 실패
  model    도구를 안 부름 · 다른 이름 · 인자에 필요한 키가 없음
  tool     (여기서는 고정 결과라 해당 없음)
  followup 도구 결과를 받은 뒤 답에 결과 값(비밀 단어)이 없음
같은 세션의 턴별 prompt / cached / timings 도 남긴다(캐시 재사용 점검의 첫 자료).

    python probe_tools.py [--base-url http://127.0.0.1:8080] [--out probe.json]
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request

SECRET = "KUMQUAT-7"
FILE = "notes/todo.txt"
TOOL_DESC = "저장소 파일 내용을 읽는다"
SCHEMA = {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}
ASK = f"{FILE} 파일에 적힌 암호 단어가 무엇인지 read_file 도구로 읽고 그 단어만 답하라."
SAMPLING = {"temperature": 0.6, "top_p": 0.95}


def post(base, path, body, key, stream):
    req = urllib.request.Request(base.rstrip("/") + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}", "x-api-key": key,
                                          "anthropic-version": "2023-06-01"})
    t0 = time.perf_counter()
    r = urllib.request.urlopen(req, timeout=600)
    if not stream:
        d = json.loads(r.read().decode("utf-8"))
        return d, None, (time.perf_counter() - t0) * 1000, None
    events, first = [], None
    for raw in r:
        line = raw.decode("utf-8").rstrip("\n")
        if not line.startswith("data:"):
            continue
        p = line[5:].strip()
        if p == "[DONE]":
            break
        if first is None:
            first = (time.perf_counter() - t0) * 1000
        try:
            events.append(json.loads(p))
        except json.JSONDecodeError:
            events.append({"_bad": p[:200]})
    return None, events, (time.perf_counter() - t0) * 1000, first


# ── Chat Completions ──────────────────────────────────────────────────────
def cc_turn(base, key, msgs, stream):
    body = {"model": "strata", "messages": msgs, "max_tokens": 2048, "stream": stream, **SAMPLING,
            "tools": [{"type": "function", "function": {"name": "read_file", "description": TOOL_DESC, "parameters": SCHEMA}}]}
    if stream:
        body["stream_options"] = {"include_usage": True}
    d, ev, ms, first = post(base, "/v1/chat/completions", body, key, stream)
    if not stream:
        m = d["choices"][0]["message"]
        return {"text": m.get("content") or "", "calls": [(c["id"], c["function"]["name"], c["function"]["arguments"]) for c in m.get("tool_calls") or []],
                "usage": d.get("usage"), "timings": d.get("timings"), "ms": ms, "first_ms": None, "pieces": None}
    text, calls, usage, timings, pieces = "", {}, None, None, 0
    for e in ev:
        if e.get("usage"):
            usage = e["usage"]
        if e.get("timings"):
            timings = e["timings"]
        for ch in e.get("choices") or []:
            dl = ch.get("delta") or {}
            text += dl.get("content") or ""
            for tc in dl.get("tool_calls") or []:
                c = calls.setdefault(tc.get("index", 0), {"id": None, "name": None, "args": ""})
                c["id"] = tc.get("id") or c["id"]
                fn = tc.get("function") or {}
                c["name"] = fn.get("name") or c["name"]
                if fn.get("arguments"):
                    c["args"] += fn["arguments"]
                    pieces += 1
    return {"text": text, "calls": [(c["id"], c["name"], c["args"]) for c in calls.values()], "usage": usage, "timings": timings,
            "ms": ms, "first_ms": first, "pieces": pieces}


def cc_run(base, key, stream):
    msgs = [{"role": "user", "content": ASK}]
    t1 = cc_turn(base, key, msgs, stream)
    turns = [t1]
    res = judge(t1)
    if res["stage"] is None:
        cid, name, args = t1["calls"][0]
        msgs += [{"role": "assistant", "content": t1["text"], "tool_calls": [{"id": cid, "type": "function", "function": {"name": name, "arguments": args}}]},
                 {"role": "tool", "tool_call_id": cid, "content": f"암호 단어: {SECRET}"}]
        t2 = cc_turn(base, key, msgs, stream)
        turns.append(t2)
        res = judge_follow(t2, res)
    return res, turns


# ── Anthropic Messages (Claude Code) ─────────────────────────────────────
def am_turn(base, key, msgs, stream):
    body = {"model": "strata", "messages": msgs, "max_tokens": 2048, "stream": stream, **SAMPLING,
            "tools": [{"name": "read_file", "description": TOOL_DESC, "input_schema": SCHEMA}]}
    d, ev, ms, first = post(base, "/v1/messages", body, key, stream)
    if not stream:
        text = "".join(b.get("text", "") for b in d["content"] if b["type"] == "text")
        calls = [(b["id"], b["name"], json.dumps(b["input"], ensure_ascii=False)) for b in d["content"] if b["type"] == "tool_use"]
        return {"text": text, "calls": calls, "usage": d.get("usage"), "timings": None, "ms": ms, "first_ms": None, "pieces": None, "raw": d["content"]}
    text, blocks, usage, pieces = "", {}, {}, 0
    for e in ev:
        t = e.get("type")
        if t == "message_start":
            usage.update((e.get("message") or {}).get("usage") or {})
        elif t == "content_block_start":
            blocks[e["index"]] = dict(e["content_block"], _json="")
        elif t == "content_block_delta":
            dl = e["delta"]
            if dl["type"] == "text_delta":
                text += dl["text"]
            elif dl["type"] == "input_json_delta":
                blocks[e["index"]]["_json"] += dl["partial_json"]
                pieces += 1
        elif t == "message_delta":
            usage.update(e.get("usage") or {})
    calls = [(b["id"], b["name"], b["_json"] or "{}") for b in blocks.values() if b.get("type") == "tool_use"]
    raw = [{k: v for k, v in b.items() if k != "_json"} | ({"input": json.loads(b["_json"] or "{}")} if b.get("type") == "tool_use" and ok_json(b["_json"]) else {})
           for b in blocks.values() if b.get("type") in ("text", "tool_use")]
    return {"text": text, "calls": calls, "usage": usage, "timings": None, "ms": ms, "first_ms": first, "pieces": pieces, "raw": raw}


def am_run(base, key, stream):
    msgs = [{"role": "user", "content": ASK}]
    t1 = am_turn(base, key, msgs, stream)
    turns = [t1]
    res = judge(t1)
    if res["stage"] is None:
        cid = t1["calls"][0][0]
        content = [b for b in t1["raw"] if b.get("type") != "thinking"]
        for b in content:
            if b.get("type") == "text":
                b.setdefault("text", t1["text"])
        msgs += [{"role": "assistant", "content": content},
                 {"role": "user", "content": [{"type": "tool_result", "tool_use_id": cid, "content": f"암호 단어: {SECRET}"}]}]
        t2 = am_turn(base, key, msgs, stream)
        turns.append(t2)
        res = judge_follow(t2, res)
    return res, turns


# ── OpenAI Responses (Codex) ─────────────────────────────────────────────
def rs_turn(base, key, inp, stream):
    body = {"model": "strata", "input": inp, "max_output_tokens": 2048, "stream": stream, **SAMPLING,
            "tools": [{"type": "function", "name": "read_file", "description": TOOL_DESC, "parameters": SCHEMA}]}
    d, ev, ms, first = post(base, "/v1/responses", body, key, stream)
    if stream:
        done = next((e for e in reversed(ev) if e.get("type") == "response.completed"), None)
        pieces = sum(1 for e in ev if e.get("type") == "response.function_call_arguments.delta")
        deltas = {}
        for e in ev:
            if e.get("type") == "response.function_call_arguments.delta":
                deltas[e.get("item_id") or e.get("output_index")] = deltas.get(e.get("item_id") or e.get("output_index"), "") + e["delta"]
        d = (done or {}).get("response") or {"output": [], "usage": None}
    else:
        pieces, deltas = None, {}
    text, calls = "", []
    for it in d.get("output") or []:
        if it.get("type") == "message":
            text += "".join(c.get("text", "") for c in it.get("content") or [] if c.get("type") == "output_text")
        elif it.get("type") == "function_call":
            args = it.get("arguments") or ""
            if stream:
                streamed = deltas.get(it.get("id")) or next(iter(deltas.values()), "")
                if streamed and streamed != args:
                    args = "__MISMATCH__" + streamed
            calls.append((it.get("call_id"), it.get("name"), args))
    return {"text": text, "calls": calls, "usage": d.get("usage"), "timings": None, "ms": ms, "first_ms": first, "pieces": pieces,
            "output": d.get("output") or []}


def rs_run(base, key, stream):
    inp = [{"role": "user", "content": ASK}]
    t1 = rs_turn(base, key, inp, stream)
    turns = [t1]
    res = judge(t1)
    if res["stage"] is None:
        cid = t1["calls"][0][0]
        inp = inp + [o for o in t1["output"] if o.get("type") in ("message", "function_call", "reasoning")] + \
            [{"type": "function_call_output", "call_id": cid, "output": f"암호 단어: {SECRET}"}]
        t2 = rs_turn(base, key, inp, stream)
        turns.append(t2)
        res = judge_follow(t2, res)
    return res, turns


# ── 판정 ─────────────────────────────────────────────────────────────────
def ok_json(s):
    try:
        return isinstance(json.loads(s), dict)
    except (json.JSONDecodeError, TypeError):
        return False


def judge(t):
    if not t["calls"]:
        return {"stage": "model", "why": "도구를 부르지 않음", "text_head": t["text"][:160]}
    cid, name, args = t["calls"][0]
    if not cid:
        return {"stage": "api", "why": "도구 호출 ID 없음"}
    if isinstance(args, str) and args.startswith("__MISMATCH__"):
        return {"stage": "api", "why": "스트림 조각을 이어 붙인 인자가 최종 인자와 다름"}
    if not ok_json(args):
        return {"stage": "api", "why": f"인자 JSON 조립 실패: {str(args)[:120]}"}
    if name != "read_file":
        return {"stage": "model", "why": f"다른 도구 이름 {name}"}
    if "path" not in json.loads(args):
        return {"stage": "model", "why": "인자에 path 없음"}
    return {"stage": None, "call_id": cid, "args": json.loads(args)}


def judge_follow(t, res):
    if t["calls"]:
        return {**res, "stage": "followup", "why": "결과를 받고도 도구를 또 부름"}
    if SECRET not in t["text"]:
        return {**res, "stage": "followup", "why": "후속 답에 결과 값이 없음", "text_head": t["text"][:160]}
    return {**res, "stage": "ok"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--out", default="probe_tools.json")
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    key = os.environ.get("STRATA_API_KEY", "strata-local")
    out = []
    for api, fn in (("chat_completions", cc_run), ("anthropic_messages", am_run), ("responses", rs_run)):
        for stream in (False, True):
            for r in range(a.repeat):
                try:
                    res, turns = fn(a.base_url, key, stream)
                except urllib.error.HTTPError as ex:
                    res, turns = {"stage": "api", "why": f"HTTP {ex.code}: {ex.read().decode('utf-8', 'replace')[:300]}"}, []
                except Exception as ex:  # noqa: BLE001
                    res, turns = {"stage": "api", "why": f"{type(ex).__name__}: {ex}"[:300]}, []
                row = {"api": api, "stream": stream, "r": r + 1, **res,
                       "turns": [{k: v for k, v in t.items() if k not in ("raw", "output")} for t in turns]}
                out.append(row)
                print(json.dumps({k: row[k] for k in ("api", "stream", "stage") if k in row} |
                                 {"why": row.get("why"), "pieces": [t.get("pieces") for t in turns],
                                  "usage": [t.get("usage") for t in turns]}, ensure_ascii=False), flush=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
