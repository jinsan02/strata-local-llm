"""T1 편집 직후 문법 검사(--syntax-check on) · T2 outline / read_symbol(--code-tools on) 자체 점검 (모델 · 서버 없이).
python selftest_tools.py <run_x3.py 폴더> [실제 파일 검사용 packaging 작업 복사본 폴더(선택)]"""
import sys, json, tempfile, pathlib, types
sys.path.insert(0, sys.argv[1])
import run_x3 as x3  # noqa: E402

fails = 0


def check(name, cond):
    global fails
    print(("ok  " if cond else "FAIL"), name)
    fails += 0 if cond else 1


SRC = '''import os


def top(a, b=1, *rest, key=None, **kw):
    return a + b


class Box:
    """상자."""

    size = 3

    @property
    def area(self):
        return self.size * self.size

    def grow(self, n):
        def helper(x):
            return x + 1
        self.size = helper(n)

    class Inner:
        def area(self):
            return 0
'''

root = pathlib.Path(tempfile.mkdtemp())
(root / "m.py").write_text(SRC, encoding="utf-8")
(root / "notes.txt").write_text("hello\n", encoding="utf-8")

# T1 꺼짐: 지금과 같음 (깨진 편집도 쓴다)
x3.SYNTAX_CHECK, x3.EDIT_APPLY = False, "lenient"
ok, out = x3.edit_file(root, {"path": "m.py", "old_string": "    return a + b\n", "new_string": "    return (a + b\n"}, ("tests",))
check("T1 off: 깨진 편집도 그대로 적용 (기존 동작)", ok and "(a + b" in (root / "m.py").read_text(encoding="utf-8"))
(root / "m.py").write_text(SRC, encoding="utf-8")

# T1 켜짐
x3.SYNTAX_CHECK = True
x3.SYNTAX_REJECTS[0] = 0
before = (root / "m.py").read_text(encoding="utf-8")
ok, out = x3.edit_file(root, {"path": "m.py", "old_string": "    return a + b\n", "new_string": "    return (a + b\n"}, ("tests",))
check("T1 on: 문법이 깨지면 거부하고 파일은 그대로", not ok and (root / "m.py").read_text(encoding="utf-8") == before)
check("T1 on: 메시지에 줄 번호 · 오류 줄 표시 · 다시 호출 안내", "줄 " in out and ">" in out and "다시 호출" in out and x3.SYNTAX_REJECTS[0] == 1)
ok, out = x3.edit_file(root, {"path": "m.py", "old_string": "    return a + b\n", "new_string": "    return a + b + 1\n"}, ("tests",))
check("T1 on: 올바른 편집은 그대로 적용", ok and "a + b + 1" in (root / "m.py").read_text(encoding="utf-8"))
ok, out = x3.edit_file(root, {"path": "m.py", "old_string": "        self.size = helper(n)\n", "new_string": "      self.size = helper(n)\n"}, ("tests",))
check("T1 on: 들여쓰기 오류(IndentationError)도 거부", not ok and "적용하지 않았다" in out)
# lenient 들여쓰기 이동으로 맞춘 편집도 검사를 거친다
ok, out = x3.edit_file(root, {"path": "m.py", "old_string": "  def grow(self, n):\n", "new_string": "  def grow(self, n:\n"}, ("tests",))
check("T1 on: 들여쓰기 이동(lenient)으로 맞춘 편집도 검사", not ok and "문법 오류" in out)
ok, out = x3.edit_file(root, {"path": "notes.txt", "old_string": "hello", "new_string": "def ("}, ("tests",))
check("T1 on: .py 가 아니면 검사하지 않음", ok)
ok, out = x3.edit_file(root, {"path": "new_mod.py", "old_string": "", "new_string": "def f(:\n"}, ("tests",))
check("T1 on: 깨진 새 파일은 만들지 않음", not ok and not (root / "new_mod.py").exists())
x3.SYNTAX_CHECK = False
(root / "m.py").write_text(SRC, encoding="utf-8")

# T2 outline
o = x3.code_tool(root, "outline", {"path": "m.py"})
lines = o.splitlines()
check("outline: 첫 줄에 경로 · 전체 줄 수", lines[0].startswith("m.py (") and "줄)" in lines[0])
check("outline: 함수 인자(*, ** 포함)", any("def top(a, b, *rest, key, **kw)" in ln for ln in lines))
check("outline: 데코레이터 줄부터 범위 시작", any(ln.strip().startswith("13-15") and "def area(self)" in ln for ln in lines))
check("outline: 함수 안 함수는 빼고 중첩 클래스는 넣음", not any("helper" in ln for ln in lines) and any("class Inner" in ln for ln in lines))

# T2 read_symbol
s = x3.code_tool(root, "read_symbol", {"path": "m.py", "name": "Box.grow"})
check("read_symbol: 클래스.메서드 전체 + 줄 번호", "Box.grow (줄 17-20)" in s and "helper(n)" in s and "   17  " in s)
s = x3.code_tool(root, "read_symbol", {"path": "m.py", "name": "top"})
check("read_symbol: 최상위 함수", "top (줄 4-5)" in s and "return a + b" in s)
s = x3.code_tool(root, "read_symbol", {"path": "m.py", "name": "area"})
check("read_symbol: 같은 이름이 여러 곳이면 골라 달라고 함", s.startswith("오류") and "Box.area" in s and "Box.Inner.area" in s)
s = x3.code_tool(root, "read_symbol", {"path": "m.py", "name": "Box.grwo"})
check("read_symbol: 없는 이름이면 비슷한 이름 제안", s.startswith("오류") and "Box.grow" in s)
check("code_tool: .py 아님 · 저장소 밖 거부",
      x3.code_tool(root, "outline", {"path": "notes.txt"}).startswith("오류") and x3.code_tool(root, "outline", {"path": "../x.py"}).startswith("오류"))
long_src = "def big():\n" + "".join(f"    x{i} = {i}\n" for i in range(500))
(root / "big.py").write_text(long_src, encoding="utf-8")
s = x3.code_tool(root, "read_symbol", {"path": "big.py", "name": "big"})
check("read_symbol: 400줄 넘으면 자르고 이어 읽을 줄 안내", "start_line=401" in s and "  400  " in s and "  401  " not in s)

# 통합: 가짜 모델이 outline → read_symbol → 깨진 편집 → 고친 편집 → 끝
seq = [("outline", {"path": "m.py"}), ("read_symbol", {"path": "m.py", "name": "top"}),
       ("edit_file", {"path": "m.py", "old_string": "    return a + b\n", "new_string": "    return (a + b\n"}),
       ("edit_file", {"path": "m.py", "old_string": "    return a + b\n", "new_string": "    return a * b\n"})]
seen_tools = []


def chat(base, key, m, mt, to, tools):
    seen_tools.append([t["function"]["name"] for t in (tools or [])])
    k = sum(1 for x in m if x["role"] == "tool")
    if tools and k < len(seq):
        fn, args = seq[k]
        msg = {"content": "", "tool_calls": [{"id": f"c{k}", "type": "function", "function": {"name": fn, "arguments": json.dumps(args)}}]}
    else:
        msg = {"content": "고쳤다"}
    return {"choices": [{"message": msg, "finish_reason": "stop"}], "usage": {"prompt_tokens": 1000, "completion_tokens": 5}}, 1.0


def run(code_tools, syntax):
    (root / "m.py").write_text(SRC, encoding="utf-8")
    seen_tools.clear()
    x3.SYNTAX_CHECK = syntax
    a = types.SimpleNamespace(max_steps=20, budget=8192, ctx=32768, timeout=10, base_url="x", force_at=22272, final_turn="none",
                              mask="off", reasoning_echo="none", tool_out="chars", code_tools=code_tools)
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
    return x3.navigate_loop(root, msgs, a, "k", ("tests",), chat=chat, counter=lambda m, t: 1000), msgs


r, msgs = run("on", True)
tool_out = [x["content"] for x in msgs if x["role"] == "tool"]
check("통합 on: 도구 목록에 outline · read_symbol", "outline" in seen_tools[0] and "read_symbol" in seen_tools[0])
check("통합 on: outline · read_symbol 결과가 모델에게 감", "class Box" in tool_out[0] and "return a + b" in tool_out[1])
check("통합 on: 깨진 편집 거부 → 다음 편집 적용", "문법 오류" in tool_out[2] and r["syntax_rejects"] == 1 and r["edit_ok"] == 1
      and "a * b" in (root / "m.py").read_text(encoding="utf-8"))
check("통합 on: code_tool_calls 2", r["code_tool_calls"] == 2)
r0, msgs0 = run("off", False)
out0 = [x["content"] for x in msgs0 if x["role"] == "tool"]
check("통합 off: 도구 목록 · 동작이 기존과 같음 (outline 은 알 수 없는 도구)", "outline" not in seen_tools[0] and out0[0].startswith("오류")
      and r0["syntax_rejects"] == 0 and r0["code_tool_calls"] == 0)

# T1 마지막 답 블록: 다 적용해서 깨지면 깨는 블록만 뺀다. 같이 있어야 맞는 블록은 그대로.
def blk(s, r):
    return f"### EDIT: m.py\n<<<<<<< SEARCH\n{s}\n=======\n{r}\n>>>>>>> REPLACE\n"


good = blk("    return a + b", "    return a - b")
bad = blk("    size = 3", "    size = (3")
x3.SYNTAX_CHECK, x3.EDIT_APPLY = True, "lenient"
(root / "m.py").write_text(SRC, encoding="utf-8")
n, errs = x3.apply_edits(root, good + "\n" + bad, ["m.py"])
t = (root / "m.py").read_text(encoding="utf-8")
check("최종 블록: 깨는 블록만 빼고 나머지는 적용", n == 1 and "a - b" in t and "size = 3" in t and any("빼고" in e for e in errs)
      and any(f.startswith("syntax_drop") for f in x3.LAST_FORMAT["flags"]))
check("최종 블록: 빼고 나면 파싱됨 → error_type 는 부분 적용 계열", x3.syntax_problem("m.py", t) is None and x3.error_type(n, errs, {"ok": True}) == "pass_partial_apply")
(root / "m.py").write_text(SRC, encoding="utf-8")
pair = blk("def top(a, b=1, *rest, key=None, **kw):\n    return a + b", "def top(a, b=1, *rest, key=None, **kw):\n    if a:") \
    + "\n" + blk("    if a:", "    if a:\n        return a + b\n    return b")
n, errs = x3.apply_edits(root, pair, ["m.py"])
t = (root / "m.py").read_text(encoding="utf-8")
check("최종 블록: 둘이 같이 있어야 맞는 블록(중간 상태는 깨짐)은 그대로 둘 다 적용", n == 2 and not errs and "return b" in t and x3.syntax_problem("m.py", t) is None)
x3.SYNTAX_CHECK = False
(root / "m.py").write_text(SRC, encoding="utf-8")
n, errs = x3.apply_edits(root, good + "\n" + bad, ["m.py"])
check("최종 블록 off: 기존처럼 둘 다 적용(깨진 채로)", n == 2 and "size = (3" in (root / "m.py").read_text(encoding="utf-8"))

# 실제 packaging 파일(선택)
if len(sys.argv) > 2:
    pk = pathlib.Path(sys.argv[2])
    o = x3.code_tool(pk, "outline", {"path": "src/packaging/metadata.py"})
    s = x3.code_tool(pk, "read_symbol", {"path": "src/packaging/metadata.py", "name": "Metadata.from_raw"})
    print(f"   실제 metadata.py: outline {len(o)}자 / {len(o.splitlines())}줄, from_raw {len(s)}자")
    check("실제 파일: outline 이 read_file 한 번(12,000자)보다 작음", len(o) < 12000 and "class Metadata" in o)
    check("실제 파일: Metadata.from_raw 를 바로 읽음", "def from_raw" in s.splitlines()[1] or "def from_raw" in s)

print("FAILS", fails)
sys.exit(1 if fails else 0)
