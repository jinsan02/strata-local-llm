"""H8 루프 통합 점검 (서버 없이 가짜 모델). python selftest_h8_loop.py <bench_dir>
A: 일찍 끝냄 -> 체크 턴(early) -> 고침 -> 끝.  B: 계속 읽기만 -> 3턴 전 알림 -> 예산 끝 체크 턴(budget) -> 도구 2턴 더 -> 강제 턴.
C: H8 꺼짐이면 예전과 같은 흐름(20번째가 강제 턴)."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent))
import run_x3 as X  # noqa: E402

NL = chr(10)
FAILS: list[str] = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


TASK = "version_bump"
tcfg = json.loads((X.TASKS / TASK / "task.json").read_text(encoding="utf-8"))
prompt = (X.TASKS / TASK / "prompt.md").read_text(encoding="utf-8")


def make_a():
    return SimpleNamespace(max_steps=20, budget=8192, ctx=65536, timeout=60, base_url="http://x", final_turn="none",
                           force_at=65536 - 8192 - 2048, tool_out="chars", reasoning_echo="none", code_tools="off",
                           mask="off", reread_guard="off", h8_task=prompt, h8_regress=list(tcfg["regress"]))


def call(i, name, args):
    return {"id": f"c{i}", "type": "function", "function": {"name": name, "arguments": json.dumps(args, ensure_ascii=False)}}


def resp(content="", calls=None):
    return ({"choices": [{"message": {"content": content, "tool_calls": calls or []}, "finish_reason": "tool_calls" if calls else "stop"}],
             "usage": {"prompt_tokens": 1000, "completion_tokens": 10}}, 5.0)


def run(script, h8_on: bool):
    root = X.fresh_copy(f"h8selftest-{'on' if h8_on else 'off'}")
    X.H8 = h8_on
    X.SYNTAX_CHECK = h8_on
    X.EDIT_APPLY = "lenient"
    seen = []

    def chat(base, key, msgs, mt, timeout, tools):
        seen.append({"tools": tools is not None, "last_role": msgs[-1]["role"], "last": str(msgs[-1].get("content") or "")[:4000]})
        return script(len(seen) - 1, msgs, tools)

    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "### 과제" + NL + prompt}]
    r = X.navigate_loop(root, msgs, make_a(), "k", deny=("tests",), chat=chat, counter=lambda m, t: 1000)
    return r, seen, msgs, root


BAD = "def helper(x):" + NL + "    return InvalidThing(x)" + NL
GOOD = "def helper(x):" + NL + "    return str(x)" + NL


def script_a(i, msgs, tools):
    if i == 0:
        return resp("", [call(0, "read_file", {"path": "src/packaging/version.py", "start_line": 1, "end_line": 5})])
    if i == 1:
        return resp("", [call(1, "edit_file", {"path": "src/packaging/h8probe.py", "old_string": "", "new_string": BAD})])
    if i == 2:
        return resp("다 했다")
    if i == 3:
        return resp("", [call(3, "edit_file", {"path": "src/packaging/h8probe.py", "old_string": "    return InvalidThing(x)", "new_string": "    return str(x)"})])
    return resp("고쳤다. 끝.")


r, seen, msgs, root = run(script_a, True)
h = r["h8"]
check("A: 일찍 끝내면 체크 턴(early)", h["trigger"] == "early" and h["trigger_step"] == 2, str({k: h[k] for k in ("trigger", "trigger_step")}))
check("A: 편집 경고 1번(InvalidThing)", h["edit_warnings"] == 1 and any("InvalidThing" in t.get("content", "") for t in msgs if t["role"] == "tool"))
chk = [m for m in msgs if m["role"] == "user" and "[하네스 점검]" in str(m["content"])]
check("A: 체크 메시지 1개, 지시문 · `bump` 없음 · 코드 검사 문제 포함", len(chk) == 1 and "`bump`" in chk[0]["content"] and "InvalidThing" in chk[0]["content"]
      and prompt.strip()[:30] in chk[0]["content"], chk[0]["content"][:600] if chk else "없음")
check("A: 체크 턴 뒤 도구 턴 1번 쓰고 끝", h["extra_tool_turns"] == 1 and r["final"].startswith("고쳤다") and len(seen) == 5, f"extra={h['extra_tool_turns']} calls={len(seen)}")
check("A: 마지막 파일은 고친 내용", (root / "src/packaging/h8probe.py").read_text(encoding="utf-8") == GOOD)
check("A: 기존 테스트 결과가 체크 메시지에", "기존 테스트" in chk[0]["content"] if chk else False)


def script_b(i, msgs, tools):
    if tools is None:
        return resp("강제 턴 답")
    return resp("", [call(i, "read_file", {"path": "src/packaging/version.py", "start_line": 1 + i, "end_line": 2 + i})])


r, seen, msgs, root = run(script_b, True)
h = r["h8"]
notice_at = [k for k, m in enumerate(msgs) if m["role"] == "tool" and "[하네스 알림]" in str(m["content"])]
check("B: 알림 1번", h["notice"] and len(notice_at) == 1)
check("B: 예산 끝 체크 턴(budget, step 19)", h["trigger"] == "budget" and h["trigger_step"] == 19, str({k: h[k] for k in ("trigger", "trigger_step")}))
check("B: 도구 턴 2번 더 쓰고 22번째가 강제 턴", h["extra_tool_turns"] == 2 and len(seen) == 22 and seen[-1]["tools"] is False and all(x["tools"] for x in seen[:21]),
      f"extra={h['extra_tool_turns']} calls={len(seen)} last_tools={seen[-1]['tools'] if seen else None}")
check("B: 19번째 요청 직전 메시지가 체크 메시지", seen[19]["last_role"] == "user" and "[하네스 점검]" in seen[19]["last"])
check("B: 강제 턴 답이 final", r["final"] == "강제 턴 답")
check("B: 바뀐 파일이 없으면 테스트를 돌리지 않음", "돌리지 않음" in (h["gate"] or {}).get("tests", ""))
check("B: forced_turns 1", r["forced_turns"] == 1)

r, seen, msgs, root = run(script_b, False)
check("C: H8 꺼짐 - 20번째가 강제 턴, 체크 · 알림 없음", len(seen) == 20 and seen[-1]["tools"] is False and r["h8"]["state"] == "off"
      and not any("[하네스" in str(m.get("content")) for m in msgs), f"calls={len(seen)}")

for d in X.RUNS.glob("h8selftest-*"):
    shutil.rmtree(d, ignore_errors=True)
print(("FAILS " + str(len(FAILS)) + ": " + ", ".join(FAILS)) if FAILS else "FAILS 0")
