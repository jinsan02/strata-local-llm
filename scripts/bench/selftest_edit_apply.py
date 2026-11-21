"""H7 편집 적용(--edit-apply lenient) 자체 점검 (모델 · 서버 없이). python selftest_edit_apply.py <run_x3.py 폴더>"""
import sys, tempfile, pathlib
sys.path.insert(0, sys.argv[1])
import run_x3 as x3  # noqa: E402

SRC = ("class V:\n    def a(self):\n        return 1\n\n    def b(self):\n"
       "        return 2" + " " * 3 + "\n")   # 6행 끝 공백 3칸 (편집기가 지우지 않게 따로 붙임)
fails = 0


def check(name, cond):
    global fails
    print(("ok  " if cond else "FAIL"), name)
    fails += 0 if cond else 1


def fresh():
    d = pathlib.Path(tempfile.mkdtemp())
    (d / "pkg").mkdir()
    (d / "pkg" / "v.py").write_text(SRC, encoding="utf-8", newline="\n")
    return d


def body(d):
    return (d / "pkg" / "v.py").read_text(encoding="utf-8")


# 1) strict(H0)는 예전 그대로: 2칸 더 들여 쓴 블록은 실패 (dedent 는 공통 들여쓰기를 다 빼서 못 맞춤)
over = "      def a(self):\n          return 1"
ans = f"### EDIT: pkg/v.py\n<<<<<<< SEARCH\n{over}\n=======\n      def a(self):\n          return 10\n>>>>>>> REPLACE"
x3.EDIT_APPLY = "strict"
d = fresh(); n, e = x3.apply_edits(d, ans, [])
check("strict: +2 들여쓰기 블록 실패", n == 0 and e)
# 2) lenient: 같은 블록이 -2 이동으로 적용, 들여쓰기는 파일에 맞게
x3.EDIT_APPLY = "lenient"
d = fresh(); n, e = x3.apply_edits(d, ans, [])
check("lenient: +2 블록 적용", n == 1 and not e and "    def a(self):\n        return 10\n" in body(d) and "indent-2" in x3.LAST_FORMAT["flags"])
# 3) edit_file 도구: 덜 들여 쓴 old_string (+4 이동)
d = fresh(); ok, msg = x3.edit_file(d, {"path": "pkg/v.py", "old_string": "def b(self):\n    return 2", "new_string": "def b(self):\n    return 20"}, ())
check("edit_file: +4 이동 적용", ok and "        return 20" in body(d) and x3.LAST_EDIT_HOW[0] == "indent+4")
# 4) 여러 곳 일치 → 줄 번호
d = fresh(); ok, msg = x3.edit_file(d, {"path": "pkg/v.py", "old_string": "        return", "new_string": "X"}, ())
check("edit_file: 여러 곳 → 줄 번호", not ok and "줄 3, 6" in msg and body(d) == SRC)
# 5) 줄 끝 공백 무시 (파일 6행 끝에 공백 3칸)
d = fresh(); ok, msg = x3.edit_file(d, {"path": "pkg/v.py", "old_string": "    def b(self):\n        return 2\n", "new_string": "    def b(self):\n        return 22\n"}, ())
check("edit_file: 줄 끝 공백 무시", ok and "return 22\n" in body(d) and x3.LAST_EDIT_HOW[0] == "rstrip")
# 6) 정확히 맞으면 예전과 같은 결과
d = fresh(); ok, msg = x3.edit_file(d, {"path": "pkg/v.py", "old_string": "        return 1\n", "new_string": "        return 11\n"}, ())
check("edit_file: 정확 일치", ok and "return 11" in body(d) and x3.LAST_EDIT_HOW[0] == "exact")
# 7) 전혀 다른 내용은 여전히 실패, 파일 그대로
d = fresh(); ok, msg = x3.edit_file(d, {"path": "pkg/v.py", "old_string": "zzz qqq", "new_string": "X"}, ())
check("edit_file: 없는 내용 실패", not ok and body(d) == SRC)
# 8) 텍스트 edit_file 호출 받기 (도구가 없는 강제 턴)
tc = ("<tool_call>\n<function=edit_file>\n<parameter=path>\npkg/v.py\n</parameter>\n<parameter=old_string>\n"
      "        return 1\n</parameter>\n<parameter=new_string>\n        return 111\n</parameter>\n</function>\n</tool_call>")
d = fresh(); n, e = x3.apply_edits(d, tc, [])
check("lenient: 텍스트 edit_file 호출 적용", n == 1 and "return 111" in body(d) and "text_call" in x3.LAST_FORMAT["flags"])
x3.EDIT_APPLY = "strict"
d = fresh(); n, e = x3.apply_edits(d, tc, [])
check("strict: 텍스트 호출은 편집 블록 없음", n == 0 and e == ["편집 블록 없음"])
# 9) 들여쓰기 이동이 두 가지로 맞으면 거절
amb = "a\n  a\n"
x3.EDIT_APPLY = "lenient"
nt, how, _ = x3.lenient_replace("x\n a\nyy\n   a\n", "a", "b")
check("lenient: 이동 모호 · 줄 중간은 거절하지 않음(정확 2회 → multi)", nt is None and how == "multi")
nt, how, _ = x3.lenient_replace("  q\n    q\n", " q", "Z")
check("lenient: 두 가지 이동이 맞으면 거절", nt is None and how in ("indent_ambiguous", "multi"))
x3.EDIT_APPLY = "strict"
print("FAILS", fails)
sys.exit(1 if fails else 0)
