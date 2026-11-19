"""run_tests 도구(Q15) 자체 점검 — 가짜 응답으로. 모델 · 서버 불필요(pytest 는 작은 회귀 파일만 0.5초 남짓).

    python selftest_run_tests.py <run_x3.py 가 있는 폴더>
확인: (1) off 면 도구 목록 · 재요청 문구가 H0 와 같다, (2) on 이면 run_tests 가 목록에 있고 통과 · 잘못된 경로 · 실패(문법 오류)
결과가 형식대로 나온다, (3) 숨은 테스트 파일은 돌릴 수 없다, (4) 전체 로그는 작업 복사본 밖에 저장된다.
"""
from __future__ import annotations

import json
import shutil
import sys
import types
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import run_x3 as x3  # noqa: E402

REGRESS = ["tests/test_dependency_groups.py", "tests/test_utils.py"]


def call(name, args, cid):
    return {"choices": [{"message": {"content": "", "tool_calls": [{"id": cid, "type": "function", "function": {
        "name": name, "arguments": json.dumps(args)}}]}, "finish_reason": "tool_calls"}], "usage": {"prompt_tokens": 100, "completion_tokens": 5}}


def text(t):
    return {"choices": [{"message": {"content": t}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 100, "completion_tokens": 5}}


def scripted(replies):
    it = iter(replies)
    seen = []

    def chat(base, key, msgs, mt, timeout, tools):
        seen.append({"tools": [t["function"]["name"] for t in (tools or [])], "last": msgs[-1].get("content", "")})
        return next(it), 1.0
    return chat, seen


def args(run_tests_fn):
    a = types.SimpleNamespace(base_url="http://fake", ctx=32768, budget=8192, timeout=60, max_steps=20, tool_out="chars",
                              reasoning_echo="none", final_turn="none")
    a.run_tests_fn = run_tests_fn
    return a


def main() -> int:
    fails = []
    # 1) off: H0 와 같은 도구 목록, run_tests 를 부르면 알 수 없는 도구
    root = x3.fresh_copy("stage-runtests-off")
    chat, seen = scripted([call("run_tests", {}, "c1"), text("끝")])
    nr = x3.navigate_loop(root, [{"role": "user", "content": "x"}], args(None), "k", ("tests",), chat=chat, counter=lambda m, t: 100)
    ok1 = seen[0]["tools"] == [t["function"]["name"] for t in x3.NAV_TOOLS] and nr["tool_log"][0]["ok"] is False \
        and "알 수 없는 도구" in seen[1]["last"] and nr["tests_runs"] == 0
    print("1 off = H0:", ok1, seen[0]["tools"])
    fails += [] if ok1 else ["1"]

    # 2) on: 통과 · 잘못된 경로 · 숨은 테스트 이름 · 문법 오류 뒤 실패 요약
    root = x3.fresh_copy("stage-runtests-on")
    (root / "tests" / "test_x3_hidden.py").write_text("def test_secret():\n    assert False\n", encoding="utf-8")  # 있어도 못 돌림
    # dependency_groups 를 실제로 깨기: 첫 줄 뒤에 문법 오류를 넣는다(edit_file 로)
    src = (root / "src/packaging/dependency_groups.py").read_text(encoding="utf-8")
    first = src.splitlines()[0]
    assert first and src.count(first) == 1, first
    chat, seen = scripted([
        call("run_tests", {}, "c1"),
        call("run_tests", {"path": "src/packaging/utils.py"}, "c2"),
        call("run_tests", {"path": "tests/../../outside.py"}, "c3"),
        call("run_tests", {"path": "tests/test_x3_hidden.py"}, "c4"),
        call("edit_file", {"path": "src/packaging/dependency_groups.py", "old_string": first, "new_string": first + "\ndef broken(:"}, "c5"),
        call("run_tests", {"path": "tests/test_dependency_groups.py"}, "c6"),
        text("끝"),
    ])
    a = args(x3.make_run_tests(REGRESS))
    nr = x3.navigate_loop(root, [{"role": "user", "content": "x"}], a, "k", ("tests",), chat=chat, counter=lambda m, t: 100)
    outs = [s["last"] for s in seen[1:]]
    logdir = root.parent / f"{root.name}_testlogs"
    ok2 = ("run_tests" in seen[0]["tools"]
           and outs[0].startswith("종료 코드 0") and "passed" in outs[0] and "재현:" in outs[0]
           and outs[1].startswith("오류") and outs[2].startswith("오류") and outs[3].startswith("오류")
           and nr["edit_ok"] == 1
           and outs[5].startswith("종료 코드 ") and not outs[5].startswith("종료 코드 0") and "첫 실패:" in outs[5]
           and "SyntaxError" in outs[5] and "secret" not in "".join(outs)
           and nr["tests_runs"] == 5 and nr["tool_errors"] == 3
           and logdir.is_dir() and len(list(logdir.glob("run*.log"))) == 2
           and not any(p.name.endswith(".log") for p in root.rglob("*.log")))
    print("2 on:", ok2, "| tests_runs", nr["tests_runs"], "tool_errors", nr["tool_errors"])
    for o in outs[:1] + outs[5:6]:
        print("   ---\n   " + o.replace("\n", "\n   ")[:700])
    fails += [] if ok2 else ["2"]

    # 3) nav_summary: off 면 tests_runs 꼬리 없음, on 이면 있음
    s_off = x3.nav_summary({**nr, "tests_runs": 0}, 1, 1)
    s_on = x3.nav_summary(nr, 1, 1)
    ok3 = "tests_runs" not in s_off and s_on.endswith("tests_runs 5")
    print("3 summary:", ok3)
    fails += [] if ok3 else ["3"]
    for d in ("stage-runtests-off", "stage-runtests-on"):
        shutil.rmtree(x3.RUNS / d, ignore_errors=True)
        shutil.rmtree(x3.RUNS / f"{d}_testlogs", ignore_errors=True)
    print("FAIL", fails or "없음 — 전부 통과")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
