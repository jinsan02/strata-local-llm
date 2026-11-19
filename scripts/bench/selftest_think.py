"""thinking 관측 기록 자체 점검 (가짜 응답, 서버 불필요). python selftest_think.py <run_x3.py 폴더>

확인: (1) 턴마다 reasoning_chars · think_cap · think_wrap · think_tok_est 가 남는다, (2) 상한 문장이 있으면 think_wraps 를 센다,
(3) 모델에 보내는 메시지에 reasoning 이 다시 들어가지 않는다(H0 그대로), (4) 원장 note 에 think_* 가 들어간다,
(5) reasoning 원문을 .jsonl 로 저장하는 줄이 있다, (6) think_cap 이 서버 규칙과 같다.
"""
import json
import shutil
import sys
import types
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import run_x3 as x3  # noqa: E402

fails = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (f"  {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


def reply(rsn, content="", call=None, ct=100):
    m = {"content": content, "reasoning_content": rsn}
    if call:
        m["tool_calls"] = [{"id": "c1", "type": "function", "function": {"name": call[0], "arguments": json.dumps(call[1])}}]
    return {"choices": [{"message": m, "finish_reason": "tool_calls" if call else "stop"}],
            "usage": {"prompt_tokens": 100, "completion_tokens": ct}}


root = x3.fresh_copy("stage-think")
r2 = "b" * 900 + "\n\n" + x3.THINK_WRAP_MARK + "\n"
replies = iter([
    reply("a" * 300, call=("list_files", {"path": "src"}), ct=120),
    reply(r2, call=("read_file", {"path": "src/packaging/version.py", "end_line": 3}), ct=400),
    reply("", content="끝", ct=3),
])
sent = []


def chat(base, key, msgs, mt, timeout, tools):
    sent.append(json.loads(json.dumps(msgs)))
    return next(replies), 1.0


a = types.SimpleNamespace(base_url="x", ctx=32768, budget=8192, timeout=60, max_steps=20, tool_out="chars",
                          reasoning_echo="none", final_turn="none", reread_guard="off", reasoning_budget=0)
nr = x3.navigate_loop(root, [{"role": "user", "content": "x"}], a, "k", ("tests",), chat=chat, counter=lambda m, t: 100)
shutil.rmtree(x3.RUNS / "stage-think", ignore_errors=True)
ts = nr["turns"]
check("턴 3개 기록", len(ts) == 3, str(len(ts)))
check("reasoning_chars", [t.get("reasoning_chars") for t in ts] == [300, len(r2), 0], str([t.get("reasoning_chars") for t in ts]))
check("think_cap 6144 (8192, answer_room)", all(t.get("think_cap") == 6144 for t in ts), str([t.get("think_cap") for t in ts]))
check("think_wrap 은 둘째 턴만", [t.get("think_wrap") for t in ts] == [False, True, False])
check("think_wraps 1", nr["think_wraps"] == 1)
e0 = ts[0]["think_tok_est"]
check("think_tok_est 범위", 0 < e0 <= 120 and ts[2]["think_tok_est"] == 0, str([t.get("think_tok_est") for t in ts]))
check("reasoning 원문 보관", [x["chars"] for x in nr["reasoning"]] == [t["reasoning_chars"] for t in ts])
check("모델에 reasoning 을 다시 보내지 않음(H0)", all("reasoning_content" not in m for ms in sent for m in ms))
s = x3.nav_summary(nr, 1, 1)
check("원장 note 에 think_*", "think_wraps 1; think_tok_est " in s and "think_turn_max_est " in s, s)
check("think_cap 규칙", (x3.think_cap(8192), x3.think_cap(2048), x3.think_cap(800), x3.think_cap(8192, 3072), x3.think_cap(8192, 7000))
      == (6144, 1536, None, 3072, 6144))
src = Path(x3.__file__).read_text(encoding="utf-8")
check(".jsonl 저장 줄", 'reasoning_r{i}.jsonl' in src)
print("FAIL 없음 — 전부 통과" if not fails else f"FAIL {len(fails)}: {fails}")
sys.exit(1 if fails else 0)
