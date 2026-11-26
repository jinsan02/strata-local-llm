"""strata_worker · mcp_server 자체 점검 (모델 없이 가짜 응답으로). GPU · 서버 불필요.

    python scripts/worker/selftest_worker.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import strata_worker as w  # noqa: E402

PY = sys.executable
TEST = f'"{PY}" -c "import calc; assert calc.add(2, 3) == 5, calc.add(2, 3); assert calc.sub(5, 3) == 2"'


def make_repo() -> Path:
    root = w.WORK / "_selftest_src"
    if root.exists():
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(root)], capture_output=True)
    root.mkdir(parents=True)
    (root / "calc.py").write_text("def add(a, b):\n    return a - b\n\n\ndef sub(a, b):\n    return a + b\n", encoding="utf-8", newline="\n")
    for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init"]):
        subprocess.run(["git", *a], cwd=root, check=True, capture_output=True)
    return root


def call(name, args, cid="c1"):
    return {"choices": [{"message": {"content": "", "tool_calls": [{"id": cid, "type": "function", "function": {
        "name": name, "arguments": args if isinstance(args, str) else json.dumps(args)}}]}, "finish_reason": "tool_calls"}],
        "usage": {"prompt_tokens": 500, "completion_tokens": 20}}


def text(t):
    return {"choices": [{"message": {"content": t}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 600, "completion_tokens": 10}}


def scripted(replies):
    it = iter(replies)
    seen = []

    def chat(base, key, msgs, mt, timeout, tools):
        seen.append(json.loads(json.dumps(msgs)))
        return next(it), 1.0
    return chat, seen


def main() -> int:
    src = make_repo()
    fails = []

    # 1) 한 번에 성공: 읽기 → 깨진 JSON(실행 안 함) → 편집 2개 → 끝
    chat, seen = scripted([
        call("read_file", {"path": "calc.py"}),
        call("edit_file", '{"path": "calc.py", "old_string": '),
        call("edit_file", {"path": "calc.py", "old_string": "return a - b", "new_string": "return a + b"}),
        call("edit_file", {"path": "calc.py", "old_string": "    return a + b\n\n\ndef sub(a, b):\n    return a + b",
                           "new_string": "    return a + b\n\n\ndef sub(a, b):\n    return a - b"}),
        text("add 와 sub 의 부호를 고쳤다"),
    ])
    r = w.delegate("calc.py 의 add 와 sub 가 반대로 계산한다. 고쳐라.", str(src), files=["calc.py"], test_cmd=TEST,
                   chat=chat, counter=lambda m, t: 500)
    ok1 = (r["status"] == "done" and r["tests"]["passed"] and r["attempts"] == 1 and "+    return a + b" in r["diff"]
           and r["stats"]["bad_json"] == 1 and "먼저 볼 파일" in seen[0][1]["content"] and (src / "calc.py").read_text(encoding="utf-8").count("a - b") == 1)
    print("1 한 번에 성공:", ok1, r["status"], r.get("diff_stat"))
    fails += [] if ok1 else ["1"]

    # 2) 테스트 실패 → 로그로 1회 보완 → 성공 (원본 저장소는 그대로)
    chat, seen = scripted([
        call("edit_file", {"path": "calc.py", "old_string": "return a - b", "new_string": "return a + b"}),
        text("add 를 고쳤다"),
        call("edit_file", {"path": "calc.py", "old_string": "    return a + b\n\n\ndef sub(a, b):\n    return a + b",
                           "new_string": "    return a + b\n\n\ndef sub(a, b):\n    return a - b"}),
        text("sub 도 고쳤다"),
    ])
    r2 = w.delegate("calc.py 의 add 와 sub 를 고쳐라.", str(src), test_cmd=TEST, chat=chat, counter=lambda m, t: 500,
                    keep_worktree=False, cfg_override={"retry": "repair"})
    repair_msg = seen[2][1]["content"] if len(seen) > 2 else ""
    ok2 = (r2["status"] == "done" and r2["attempts"] == 2 and "이전 시도" in repair_msg and "AssertionError" in repair_msg
           and r2["worktree"] == "삭제")
    print("2 보완 후 성공:", ok2, r2["status"], r2.get("attempts"))
    fails += [] if ok2 else ["2"]

    # 3) 저장소 밖 · .git 편집 거부, 변경 없음
    chat, _ = scripted([call("edit_file", {"path": "../evil.py", "old_string": "", "new_string": "x"}),
                        call("edit_file", {"path": ".git/config", "old_string": "", "new_string": "x"}), text("못 고쳤다")])
    r3 = w.delegate("아무거나", str(src), chat=chat, counter=lambda m, t: 500, keep_worktree=False)
    ok3 = r3["status"] == "no_change" and r3["stats"]["edit_fail"] == 2 and not (w.WORK / "evil.py").exists()
    print("3 경로 거부:", ok3, r3["status"])
    fails += [] if ok3 else ["3"]

    # 4) 잠금: 다른 살아 있는 프로세스가 잡고 있으면 busy
    w.WORK.mkdir(parents=True, exist_ok=True)
    p = subprocess.Popen([PY, "-c", "import time; time.sleep(30)"])
    w.LOCK.write_text(f"{p.pid} test", encoding="utf-8")
    r4 = w.delegate("x", str(src), chat=lambda *a: None)
    p.kill()
    ok4 = r4["status"] == "busy" and w.LOCK.exists()
    w.LOCK.unlink(missing_ok=True)
    print("4 잠금:", ok4, r4["status"])
    fails += [] if ok4 else ["4"]

    # 5) MCP: initialize · tools/list · worker_status · 없는 메서드 · discard 형식 검사
    reqs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "worker_status", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 4, "method": "nope"},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "discard_worktree", "arguments": {"worker_id": "..\\x"}}}]
    pr = subprocess.run([PY, str(HERE / "mcp_server.py")], input="\n".join(json.dumps(q, ensure_ascii=False) for q in reqs) + "\n",
                        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    resp = [json.loads(ln) for ln in pr.stdout.splitlines() if ln.strip()]
    by = {x["id"]: x for x in resp}
    st = json.loads(by[3]["result"]["content"][0]["text"]) if 3 in by else {}
    ok5 = (len(resp) == 5 and by[1]["result"]["serverInfo"]["name"] == "strata-worker"
           and [t["name"] for t in by[2]["result"]["tools"]] == ["delegate_code_task", "worker_status", "discard_worktree"]
           and "cfg" in st and by[4]["error"]["code"] == -32601 and by[5]["result"]["isError"] is True)
    print("5 MCP 프로토콜:", ok5, "server:", st.get("server"))
    fails += [] if ok5 else ["5"]
    if not ok5:
        print(pr.stdout[-1500:], pr.stderr[-1500:])

    # 6) 자동 올리기: medium 실패 → 변경을 버리고 high 로 처음부터 → 성공 (11-22)
    esc = {"ctx": 65536, "effort": "medium", "max_effort": "xhigh", "retry": "escalate", "repair": 1,
           "sampling": "card-coding", "edit_apply": "lenient"}
    chat, seen = scripted([
        call("edit_file", {"path": "calc.py", "old_string": "return a - b", "new_string": "return a + b"}),
        text("add 를 고쳤다"),
        call("read_file", {"path": "calc.py"}),
        call("edit_file", {"path": "calc.py", "old_string": "return a - b", "new_string": "return a + b"}),
        call("edit_file", {"path": "calc.py", "old_string": "    return a + b\n\n\ndef sub(a, b):\n    return a + b",
                           "new_string": "    return a + b\n\n\ndef sub(a, b):\n    return a - b"}),
        text("둘 다 고쳤다"),
    ])
    r6 = w.delegate("calc.py 의 add 와 sub 를 고쳐라.", str(src), test_cmd=TEST, chat=chat, counter=lambda m, t: 500,
                    keep_worktree=False, cfg_override=esc)
    log6 = json.loads(Path(r6["log"]).read_text(encoding="utf-8")) if r6.get("log") else {}
    att = log6.get("attempts", [])
    second_first = seen[2][1]["content"] if len(seen) > 2 else ""
    read_back = next((m["content"] for m in seen[3] if m.get("role") == "tool"), "") if len(seen) > 3 else ""
    ok6 = (r6["status"] == "done" and r6["efforts_tried"] == ["medium", "high"] and "이전 시도" not in second_first
           and "return a - b" in read_back and [x["force_at"] for x in att] == [22272, 55296]
           and [x["max_steps"] for x in att] == [20, 20] and log6.get("ladder") == ["medium", "high", "xhigh"])
    print("6 자동 올리기:", ok6, r6["status"], r6.get("efforts_tried"), [x.get("force_at") for x in att])
    fails += [] if ok6 else ["6"]

    # 7) 설정 반영 · 잘못된 노력치 · 테스트 없으면 다시 시도 안 함
    r7 = w.delegate("x", str(src), chat=lambda *a: None, effort="ultra")
    ladder_none = w.effort_ladder("low", w.load_cfg(esc), None, None)
    ladder_top = w.effort_ladder("xhigh", w.load_cfg(esc), "t", None)
    ok7 = (r7["status"] == "error" and "effort" in r7["error"] and w.x3.EDIT_APPLY == "lenient"
           and ladder_none == ["low"] and ladder_top == ["xhigh"]
           and w.effort_ladder("medium", w.load_cfg({**esc, "max_effort": "high"}), "t", None) == ["medium", "high"]
           and w.effort_ladder("medium", w.load_cfg(esc), "t", False) == ["medium"])
    print("7 설정 · 사다리:", ok7, r7.get("status"), ladder_none, ladder_top)
    fails += [] if ok7 else ["7"]

    # 8) 위임 전 확인 (11-24 A안): 파일 4개 · 없는 파일 · 문맥 초과 → rejected(+handoff), force 면 진행, 경고
    r8a = w.delegate("calc.py 의 add 를 고쳐라. 음수도 처리한다.", str(src), files=["calc.py", "a.py", "b.py", "c.py"],
                     test_cmd=TEST, chat=lambda *a: None)
    r8b = w.delegate("calc.py 의 add 를 고쳐라. 음수도 처리한다.", str(src), files=["calc.py"], test_cmd=TEST,
                     chat=lambda *a: None, cfg_override={"ctx": 20})
    chat, _ = scripted([text("고칠 것이 없다")])
    r8c = w.delegate("x", str(src), files=["nope.py"], chat=chat, counter=lambda m, t: 500, keep_worktree=False, force=True)
    pre_tw = w.precheck("tests/test_calc.py 에 add 테스트를 작성하라", str(src), None, ["tests/test_calc.py"], None, w.load_cfg())
    ok8 = (r8a["status"] == "rejected" and any("4개" in x for x in r8a["reasons"]) and len(r8a["reasons"]) == 4
           and r8a["handoff"]["to"] == "conductor" and "warnings" not in r8a
           and r8b["status"] == "rejected" and any("토큰" in x for x in r8b["reasons"])
           and r8c["status"] == "no_change" and r8c["forced_past"] and r8c["handoff"]["to"] == "conductor"
           and len(r8c["warnings"]) == 2 and len(pre_tw["warnings"]) == 2 and any("테스트 작성" in x for x in pre_tw["warnings"])
           and (w.LOGS / "route.jsonl").is_file())
    print("8 위임 전 확인:", ok8, r8a["status"], len(r8a.get("reasons", [])), r8b["status"], r8c["status"], len(pre_tw["warnings"]))
    fails += [] if ok8 else ["8"]

    # 9) 테스트 실패 → handoff 로 지휘자에게, 성공이면 handoff 없음
    chat, _ = scripted([call("edit_file", {"path": "calc.py", "old_string": "return a - b", "new_string": "return a + b"}),
                        text("add 만 고쳤다")])
    r9 = w.delegate("calc.py 의 add 와 sub 가 반대로 계산한다. 고쳐라.", str(src), files=["calc.py"], test_cmd=TEST, chat=chat,
                    counter=lambda m, t: 500, keep_worktree=False, repair=False, cfg_override={"retry": "repair"})
    ok9 = (r9["status"] == "tests_failed" and r9["handoff"]["to"] == "conductor" and "tests.tail" in r9["handoff"]["next"]
           and "handoff" not in r and "warnings" not in r)
    print("9 실패 넘기기:", ok9, r9["status"])
    fails += [] if ok9 else ["9"]

    # 정리
    w.drop_tree(r["worker_id"])
    subprocess.run(["git", "worktree", "prune"], cwd=src, capture_output=True)
    subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(src)], capture_output=True)
    print("FAIL", fails if fails else "없음 — 전부 통과")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
