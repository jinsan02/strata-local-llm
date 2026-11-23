"""Y 세트 하네스 점검 (서버 없이 가짜 모델). python selftest_y.py [bench_dir]
1) use_repo · fresh_copy(setup): 버그가 커밋으로 들어가 작업 트리 diff 가 비어 있음
2) Y3: write_allow 경로는 tests/ 아래라도 만들 수 있고, 다른 tests/ 파일은 거절. 참조 테스트를 쓰면 돌연변이 채점 통과
3) Y6(flask): 가짜 모델이 edit_file 로 참조 구현을 넣으면 숨은 테스트 통과
4) x3 세트 기본값은 예전과 같음"""
from __future__ import annotations

import json
import shutil
import subprocess
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


check("x3 기본값", X.TASKS == X.TASK_SETS["x3"] and X.REPO_LABEL == "pypa/packaging" and X.COMMIT == "6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc")
Y = X.TASK_SETS["y"]
X.TASKS = Y


def cfg(t):
    return json.loads((Y / t / "task.json").read_text(encoding="utf-8"))


def a_ns():
    return SimpleNamespace(max_steps=20, budget=8192, ctx=65536, timeout=60, base_url="http://x", final_turn="none",
                           force_at=65536 - 8192 - 2048, tool_out="chars", reasoning_echo="none", code_tools="off",
                           mask="off", reread_guard="off", h8_task="", h8_regress=[])


def call(i, name, args):
    return {"id": f"c{i}", "type": "function", "function": {"name": name, "arguments": json.dumps(args, ensure_ascii=False)}}


def resp(content="", calls=None):
    return ({"choices": [{"message": {"content": content, "tool_calls": calls or []}, "finish_reason": "tool_calls" if calls else "stop"}],
             "usage": {"prompt_tokens": 1000, "completion_tokens": 10}}, 5.0)


def loop(root, script):
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "t"}]
    X.H8 = False
    return X.navigate_loop(root, msgs, a_ns(), "k", deny=("tests",), chat=lambda b, k, m, mt, to, tools: script(len([x for x in m if x["role"] == "assistant"])),
                           counter=lambda m, t: 1000)


# 1) setup
t1 = cfg("y1_version_postdev_order")
X.use_repo("packaging")
r1 = X.fresh_copy("ytest-y1", Y / "y1_version_postdev_order" / t1["setup_patch"])
vtxt = (r1 / "src/packaging/version.py").read_text(encoding="utf-8")
st = subprocess.run(["git", "-C", str(r1), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
log = subprocess.run(["git", "-C", str(r1), "log", "--format=%s", "-2"], capture_output=True, text=True).stdout.split()
check("setup: 버그가 들어감 · 작업 트리 깨끗 · setup 커밋", "if pre is None and dev is not None:" in vtxt and st == "" and log[0] == "setup", f"{st!r} {log}")

# 2) Y3 쓰기 허용 + 돌연변이 채점
t3 = cfg("y3_tests_canonicalize_version")
X.WRITE_ALLOW = set(t3["write_allow"])
r3 = X.fresh_copy("ytest-y3")
ref_test = (Y / "y3_tests_canonicalize_version" / "private" / "ref_test.py").read_text(encoding="utf-8")


def s3(i):
    if i == 0:
        return resp("", [call(0, "edit_file", {"path": "tests/test_utils.py", "old_string": "import", "new_string": "import"})])
    if i == 1:
        return resp("", [call(1, "edit_file", {"path": t3["test_file"], "old_string": "", "new_string": ref_test})])
    return resp("끝")


nr = loop(r3, s3)
outs = [str(m.get("content")) for m in []]
check("Y3: 다른 tests 파일은 거절, 허용 경로는 만들기 성공", nr["edit_fail"] == 1 and nr["edit_ok"] == 1 and (r3 / t3["test_file"]).is_file(), f"ok {nr['edit_ok']} fail {nr['edit_fail']}")
g3 = X.grade(r3, t3, 10)
check("Y3: 참조 테스트 → 돌연변이 10/10 · 통과", g3["ok"] and g3["hidden"] == "10/10", g3["hidden"])
wrong = "from packaging.utils import canonicalize_version" + NL + NL + NL + "def test_wrong():" + NL + '    assert canonicalize_version("1.0.0a1") == "1.0.0a1"' + NL
(r3 / t3["test_file"]).write_text(wrong, encoding="utf-8", newline=NL)
gw = X.grade(r3, t3, 10)
check("Y3 분류: 기대값이 틀린 테스트 → test_fail", X.error_type(1, [], gw) == "test_fail", X.error_type(1, [], gw))
(r3 / t3["test_file"]).write_text("def test_x(:" + NL, encoding="utf-8", newline=NL)
gs = X.grade(r3, t3, 10)
check("Y3 분류: 문법이 깨진 테스트 → import_or_syntax", X.error_type(1, [], gs) == "import_or_syntax", X.error_type(1, [], gs))
X.WRITE_ALLOW = set()
check("Y3: 허용 목록을 비우면 같은 경로도 거절", not X.edit_file(r3, {"path": "tests/test_y_other.py", "old_string": "", "new_string": "x = 1" + NL}, ("tests",))[0])

# 3) Y6 flask
t6 = cfg("y6_config_require")
X.use_repo("flask")
check("use_repo(flask)", X.REPO_LABEL == "pallets/flask" and "swe_flask_5014" in X.PYX and X.COMMIT.startswith("7ee9ceb"))
r6 = X.fresh_copy("ytest-y6")
patch = (Y / "y6_config_require" / "private" / "ref.patch").read_text(encoding="utf-8")
added = NL.join(l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++"))


def s6(i):
    if i == 0:
        return resp("", [call(0, "read_file", {"path": "src/flask/config.py", "start_line": 330, "end_line": 345})])
    if i == 1:
        return resp("", [call(1, "edit_file", {"path": "src/flask/config.py", "old_string": "    def __repr__(self) -> str:",
                                                "new_string": added + NL + "    def __repr__(self) -> str:"})])
    return resp("끝")


nr6 = loop(r6, s6)
g6 = X.grade(r6, t6, 14)
check("Y6: edit_file 로 참조 구현 → 숨은 14/14 · 회귀 통과", nr6["edit_ok"] == 1 and g6["ok"] and g6["hidden"] == "14/14", f"{g6['hidden']} {g6['regress']}")

X.use_repo("packaging")
X.TASKS = X.TASK_SETS["x3"]
for d in X.RUNS.glob("ytest-*"):
    shutil.rmtree(d, ignore_errors=True)
print(("FAILS " + str(len(FAILS)) + ": " + ", ".join(FAILS)) if FAILS else "FAILS 0")
