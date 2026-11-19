"""C1 반복 읽기 막기 자체 점검 (가짜 응답). python selftest_reread.py <run_x3.py 폴더>"""
import json
import shutil
import sys
import types

sys.path.insert(0, sys.argv[1])
import run_x3 as x3  # noqa: E402


def call(name, args, cid):
    return {"choices": [{"message": {"content": "", "tool_calls": [{"id": cid, "type": "function", "function": {
        "name": name, "arguments": json.dumps(args)}}]}, "finish_reason": "tool_calls"}], "usage": {"prompt_tokens": 100, "completion_tokens": 5}}


def text(t):
    return {"choices": [{"message": {"content": t}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 100, "completion_tokens": 5}}


def run(guard, tool_out):
    root = x3.fresh_copy(f"stage-reread-{guard}-{tool_out}")
    rel = "src/packaging/dependency_groups.py"
    first = (root / rel).read_text(encoding="utf-8").splitlines()[0]
    replies = iter([
        call("read_file", {"path": rel}, "c1"),
        call("read_file", {"path": rel}, "c2"),                                  # 같은 범위 · 같은 내용
        call("read_file", {"path": rel, "start_line": 5, "end_line": 20}, "c3"),  # 다른 범위
        call("edit_file", {"path": rel, "old_string": first, "new_string": first + "\n# touched"}, "c4"),
        call("read_file", {"path": rel}, "c5"),                                  # 편집 뒤: 다시 보여 줘야 함
        call("read_file", {"path": "src/packaging/nope.py"}, "c6"),              # 없는 파일: 오류 그대로
        text("끝"),
    ])
    outs = []

    def chat(base, key, msgs, mt, timeout, tools):
        if msgs and msgs[-1].get("role") == "tool":
            outs.append(msgs[-1]["content"])
        return next(replies), 1.0

    a = types.SimpleNamespace(base_url="x", ctx=32768, budget=8192, timeout=60, max_steps=20, tool_out=tool_out,
                              reasoning_echo="none", final_turn="none", reread_guard=guard)
    nr = x3.navigate_loop(root, [{"role": "user", "content": "x"}], a, "k", ("tests",), chat=chat, counter=lambda m, t: 100)
    shutil.rmtree(x3.RUNS / f"stage-reread-{guard}-{tool_out}", ignore_errors=True)
    return outs, nr


fails = []
for tool_out in ("chars", "paged"):
    outs, nr = run("on", tool_out)
    c_on = (outs[1].startswith("(이미 본 내용: 턴 0") and not outs[2].startswith("(이미") and not outs[4].startswith("(이미")
            and "# touched" in outs[4] and outs[5].startswith("오류") and nr["reread_skips"] == 1
            and sum(1 for t in nr["tool_log"] if isinstance(t["args"], dict) and t["args"].get("reread_guard")) == 1)
    outs_off, nr_off = run("off", tool_out)
    c_off = outs_off[1] == outs_off[0] and nr_off["reread_skips"] == 0
    print(tool_out, "on:", c_on, "| off = 지금과 같음:", c_off)
    fails += [] if c_on else [f"{tool_out}-on"]
    fails += [] if c_off else [f"{tool_out}-off"]
s = x3.nav_summary({**nr, "reread_skips": 1}, 1, 1)
print("summary tail:", s[-40:])
fails += [] if s.endswith("reread_skips 1") else ["summary"]
print("FAIL", fails or "없음 — 전부 통과")
raise SystemExit(1 if fails else 0)
