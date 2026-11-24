"""H11 루프 점검 (서버 없이 가짜 모델). python selftest_h11.py <bench_dir>
A: H11 켬 — 정의 안 된 이름을 쓰는 편집 → 도구 결과에 경고, h11_warns 1. 체크 턴 · 알림은 없음(H8 꺼짐).
B: H11 켬 — 정상 편집 → 경고 없음.   C: H11 꺼짐 — 같은 나쁜 편집에도 경고 없음."""
from __future__ import annotations

import json
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
prompt = (X.TASKS / TASK / "prompt.md").read_text(encoding="utf-8")


def make_a():
    return SimpleNamespace(max_steps=20, budget=8192, ctx=65536, timeout=60, base_url="http://x", final_turn="none",
                           force_at=65536 - 8192 - 2048, tool_out="chars", reasoning_echo="none", code_tools="off",
                           mask="off", reread_guard="off")


def call(i, name, args):
    return {"id": f"c{i}", "type": "function", "function": {"name": name, "arguments": json.dumps(args, ensure_ascii=False)}}


def resp(content="", calls=None):
    return ({"choices": [{"message": {"content": content, "tool_calls": calls or []}, "finish_reason": "tool_calls" if calls else "stop"}],
             "usage": {"prompt_tokens": 1000, "completion_tokens": 10}}, 5.0)


def run(new_text: str, h11: bool, tag: str):
    root = X.fresh_copy(f"h11selftest-{tag}")
    X.H8, X.H11, X.SYNTAX_CHECK, X.EDIT_APPLY = False, h11, False, "lenient"
    steps = [resp("", [call(0, "edit_file", {"path": "src/packaging/h11probe.py", "old_string": "", "new_string": new_text})]),
             resp("끝")]

    def chat(base, key, msgs, mt, timeout, tools):
        return steps.pop(0) if steps else resp("끝")

    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "### 과제" + NL + prompt}]
    r = X.navigate_loop(root, msgs, make_a(), "k", deny=("tests",), chat=chat, counter=lambda m, t: 1000)
    tool_txt = " ".join(str(m.get("content") or "") for m in msgs if m.get("role") == "tool")
    return r, tool_txt


BAD = "def helper(x):" + NL + "    return InvalidThing(x)" + NL
GOOD = "def helper(x):" + NL + "    return str(x)" + NL
r, t = run(BAD, True, "a")
check("A: 경고가 도구 결과에", "[하네스 검사]" in t and "InvalidThing" in t, t[-300:])
check("A: h11_warns 1 · 체크 턴 없음", r["h11_warns"] == 1 and r["h8"]["trigger"] in (None, "none"), str((r["h11_warns"], r["h8"].get("trigger"))))
r, t = run(GOOD, True, "b")
check("B: 정상 편집은 경고 없음", "[하네스 검사]" not in t and r["h11_warns"] == 0)
r, t = run(BAD, False, "c")
check("C: H11 꺼짐이면 경고 없음", "[하네스 검사]" not in t and r["h11_warns"] == 0)
X.H11 = False
print("FAILS", len(FAILS))
sys.exit(1 if FAILS else 0)
