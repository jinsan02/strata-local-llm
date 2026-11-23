"""H10 점검 (서버 없이). python selftest_h10.py [bench_dir]
a) 이미 적용된 블록: H10 이면 오류 없음(already_applied), 끄면 예전처럼 오류
b) 관대한 적용이 문법을 깨면: H10 이면 마지막 답 블록 거절 · edit_file 오류, 끄면 예전처럼 적용
c) 자기가 만든 파일: H10 이면 old_string 빈 값으로 다시 쓰기, 저장소에 원래 있던 파일 · H10 끔은 거절"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent))
import run_x3 as X  # noqa: E402

NL = chr(10)
FAILS: list[str] = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


SRC = NL.join(["class A:", "    def f(self):", "        return 1", "", "    def g(self):", "        return 2", ""])
NEW_G = NL.join(["    def g(self):", "        return 3"])


def fresh():
    d = Path(tempfile.mkdtemp(prefix="h10st-"))
    (d / "pkg").mkdir()
    (d / "pkg" / "m.py").write_text(SRC, encoding="utf-8", newline=NL)
    return d


def blk(path, s, r):
    return f"### EDIT: {path}" + NL + "<<<<<<< SEARCH" + NL + s + NL + "=======" + NL + r + NL + ">>>>>>> REPLACE" + NL


X.EDIT_APPLY = "lenient"
X.EDIT_STRIP = True
X.SYNTAX_CHECK = False
OLD_G = NL.join(["    def g(self):", "        return 2"])

# a) 같은 블록 두 번: 첫째는 적용, 둘째는 이미 적용됨
ans = blk("pkg/m.py", OLD_G, NEW_G) + NL + blk("pkg/m.py", OLD_G, NEW_G)
for on in (False, True):
    X.H10 = on
    d = fresh()
    applied, errs = X.apply_edits(d, ans, ["pkg/m.py"])
    flags = X.LAST_FORMAT.get("flags", [])
    if on:
        check("a: H10 이면 두 번째 블록은 이미 적용됨(오류 없음)", applied == 1 and not errs and "already_applied" in flags, f"{applied} {errs} {flags}")
    else:
        check("a: 끄면 예전처럼 오류 1개", applied == 1 and len(errs) == 1, f"{applied} {errs}")
    shutil.rmtree(d, ignore_errors=True)

# a') 진짜로 안 맞는 블록은 H10 이어도 오류
X.H10 = True
d = fresh()
applied, errs = X.apply_edits(d, blk("pkg/m.py", "    def zzz(self):", "    def yyy(self):"), ["pkg/m.py"])
check("a: 진짜 안 맞는 블록은 H10 이어도 오류", applied == 0 and len(errs) == 1, f"{applied} {errs}")
shutil.rmtree(d, ignore_errors=True)

# b) SEARCH 전체 +2, 새 메서드는 제 칸수 → 들여쓰기 이동(-2) 하면 새 메서드가 2칸이 되어 깨짐
s_bad = NL.join(["          return 1"])
r_bad = NL.join(["          return 1", "", "    def h(self):", "        return 9"])
for on in (False, True):
    X.H10 = on
    d = fresh()
    applied, errs = X.apply_edits(d, blk("pkg/m.py", s_bad, r_bad), ["pkg/m.py"])
    txt = (d / "pkg" / "m.py").read_text(encoding="utf-8")
    broke = X._py_breaks("pkg/m.py", SRC, txt)
    if on:
        check("b: H10 이면 깨는 블록 거절, 파일 그대로", applied == 0 and txt == SRC and "h10_syntax_reject" in X.LAST_FORMAT.get("flags", []), f"{applied} {X.LAST_FORMAT}")
        ok, out = X.edit_file(d, {"path": "pkg/m.py", "old_string": s_bad, "new_string": r_bad}, ("tests",))
        check("b: H10 이면 edit_file 도 거절 · 안내", not ok and "문법이 깨진다" in out and txt == (d / "pkg" / "m.py").read_text(encoding="utf-8"), out[:120])
    else:
        check("b: 끄면 예전처럼 적용되어 파일이 깨짐(재현)", applied == 1 and broke, f"{applied} broke={broke}")
    shutil.rmtree(d, ignore_errors=True)

# b') 관대한 적용이지만 문법이 맞으면 H10 이어도 적용
X.H10 = True
d = fresh()
applied, errs = X.apply_edits(d, blk("pkg/m.py", "          return 1", "          return 5"), ["pkg/m.py"])
check("b: 문법이 맞는 들여쓰기 이동은 그대로 적용", applied == 1 and "return 5" in (d / "pkg" / "m.py").read_text(encoding="utf-8"), f"{applied} {errs}")
shutil.rmtree(d, ignore_errors=True)

# c) 자기가 만든 파일 다시 쓰기
for on in (False, True):
    X.H10 = on
    X.CREATED_FILES.clear()
    d = fresh()
    ok1, _ = X.edit_file(d, {"path": "pkg/new.py", "old_string": "", "new_string": "x = 1" + NL}, ("tests",))
    ok2, out2 = X.edit_file(d, {"path": "pkg/new.py", "old_string": "", "new_string": "x = 2" + NL}, ("tests",))
    ok3, _ = X.edit_file(d, {"path": "pkg/m.py", "old_string": "", "new_string": "y = 1" + NL}, ("tests",))
    body = (d / "pkg" / "new.py").read_text(encoding="utf-8")
    if on:
        check("c: H10 이면 자기가 만든 파일을 통째로 다시 씀", ok1 and ok2 and body == "x = 2" + NL and "다시 썼다" in out2, out2)
        check("c: 원래 있던 파일은 H10 이어도 거절", not ok3 and (d / "pkg" / "m.py").read_text(encoding="utf-8") == SRC)
    else:
        check("c: 끄면 예전처럼 거절", ok1 and not ok2 and body == "x = 1" + NL)
    shutil.rmtree(d, ignore_errors=True)

X.H10 = False
X.CREATED_FILES.clear()
X.EDIT_APPLY = "strict"
X.EDIT_STRIP = False
print(("FAILS " + str(len(FAILS)) + ": " + ", ".join(FAILS)) if FAILS else "FAILS 0")
