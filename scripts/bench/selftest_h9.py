"""H9 (--edit-strip on) 점검. 서버 없이. python selftest_h9.py [bench_dir]
1) 단위: 첫 줄만 +2 · 일부 줄 +2 · 여러 곳 일치 · 탭 · 빼야 할 공백 부족 · 의도한 들여쓰기 변경 유지 · 꺼지면 예전과 같음
2) 지난 실행에서 '공백만 틀린' 실패 편집을 원본에 같은 내용(new = old)으로 적용하면 원본과 글자까지 같아야 한다
3) 지난 실행의 성공한 편집 old_string 은 H9 를 켜도 같은 방법(exact 등)으로 맞는다(앞 단계 우선)"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent))
import run_x3 as X  # noqa: E402

NL = chr(10)
FAILS: list[str] = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


SRC = NL.join([
    "class A:",
    "    def f(self, x):",
    "        if x:",
    "            return 1",
    "        return _evaluate(self._m, x)",
    "",
    "",
    "def g(y):",
    "    return y",
    "",
])

X.EDIT_STRIP = False
nt, how, _ = X.lenient_replace(SRC, "          return _evaluate(self._m, x)" + NL + NL + NL + "def g(y):", "X")
check("꺼짐: 첫 줄만 +2 는 예전처럼 none", nt is None and how == "none", how)

X.EDIT_STRIP = True
old = "          return _evaluate(self._m, x)" + NL + NL + NL + "def g(y):"
new = "          return _evaluate(self._m, x)" + NL + NL + "    def h(self):" + NL + "        return 2" + NL + NL + NL + "def g(y):"
nt, how, _ = X.lenient_replace(SRC, old, new)
want = SRC.replace("        return _evaluate(self._m, x)" + NL + NL + NL + "def g(y):",
                   "        return _evaluate(self._m, x)" + NL + NL + "    def h(self):" + NL + "        return 2" + NL + NL + NL + "def g(y):")
check("첫 줄만 +2: strip 으로 적용, 첫 줄은 파일 칸수 · 새 줄은 그대로", how == "strip" and nt == want, repr(nt))
ast.parse(nt or "")

old = NL.join(["          if x:", "              return 1", "        return _evaluate(self._m, x)"])
new = NL.join(["          if x:", "              return 3", "        return _evaluate(self._m, x)"])
nt, how, _ = X.lenient_replace(SRC, old, new)
check("일부 줄 +2(최빈값 +2 → 파일 기준 -2): 적용", how == "strip" and nt == SRC.replace("            return 1", "            return 3"), repr(nt))

src2 = SRC + NL.join(["def k(z):", "    return y", ""])
nt, how, _ = X.lenient_replace(src2, "  return y", "  return q")
check("여러 곳 일치면 적용 안 함", nt is None, how)

nt, how, _ = X.lenient_replace(SRC, "      if x:" + NL + chr(9) + "return 1", "z")
check("탭이 섞이면 적용 안 함", nt is None, how)

old = NL.join(["  def f(self, x):", "      if x:"])
nt, how, _ = X.lenient_replace(SRC, old, old)
check("파일 들여쓰기 쪽으로 옮김(+2) 결과 원본과 같음", how in ("indent+2", "strip") and nt == SRC, how)

old = NL.join(["        return _evaluate(self._m, x)", "", "  ", "def g(y):"])
new = NL.join(["        return _evaluate(self._m, x)", "", "def g(y):", "    y = y + 1"])
nt, how, _ = X.lenient_replace(SRC.replace(NL + NL + "def g", NL + "    " + NL + "def g"), old, new)
check("빈 줄 공백 차이(줄 끝 공백) 는 앞 단계(rstrip) 또는 strip 으로 적용", nt is not None, how)

old = NL.join(["    if x:", "        return 1"])
new = NL.join(["    if x:", "        return 1", "    else:", "        return 0"])
nt, how, _ = X.lenient_replace(SRC, old, new)
check("블록 전체 -4 는 앞 단계 indent 가 처리(strip 아님)", how == "indent+4", how)

# ── 2) 지난 실행 재현 ──
COMMIT = X.COMMIT
cache: dict[str, str | None] = {}


def original(path):
    if path not in cache:
        r = subprocess.run(["git", "-C", str(X.SRC), "show", COMMIT + ":" + path], capture_output=True)
        cache[path] = r.stdout.decode("utf-8") if r.returncode == 0 else None
    return cache[path]


rescued = identical = parsed = 0
kept_same = changed_how = 0
for d in sorted((X.ROOT / "experiments" / "runs").iterdir()) if hasattr(X, "ROOT") else sorted((Path(__file__).resolve().parents[2] / "experiments" / "runs").iterdir()):
    if "_nav_" not in d.name:
        continue
    for f in sorted(d.glob("tools_r*.json")):
        try:
            tools = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        before: set[str] = set()
        for c in tools:
            a = c.get("args") or {}
            if c.get("tool") != "edit_file" or "old_string" not in a or "ok" not in c:
                continue
            path = a.get("path") or ""
            text = original(path)
            old_s = a.get("old_string") or ""
            if c["ok"]:
                if text is not None and path not in before and old_s.strip():
                    X.EDIT_STRIP = False
                    _, h0, _ = X.lenient_replace(text, old_s, old_s)
                    X.EDIT_STRIP = True
                    _, h1, _ = X.lenient_replace(text, old_s, old_s)
                    if h0 != "none":
                        kept_same += h0 == h1
                        changed_how += h0 != h1
                before.add(path)
                continue
            if text is None or path in before or a.get("how") not in ("none", None) or not old_s.strip():
                continue
            nt, h, _ = X.lenient_replace(text, old_s, old_s)
            if h == "strip":
                rescued += 1
                identical += nt == text
                try:
                    ast.parse(nt)
                    parsed += 1
                except SyntaxError:
                    pass
print(f"재현: 공백만 틀린 실패 편집 {rescued}건 적용, 원본과 같음 {identical}, 파싱 {parsed}; 성공 편집 방법 유지 {kept_same}, 바뀜 {changed_how}")
check("재현: 7건 이상 적용(원본 기준 근사 없는 것)", rescued >= 7, str(rescued))
check("재현: new = old 적용 결과가 모두 원본과 글자까지 같음", rescued and identical == rescued, f"{identical}/{rescued}")
check("재현: 성공했던 편집은 H9 를 켜도 방법이 그대로", changed_how == 0 and kept_same > 0, f"same {kept_same} changed {changed_how}")
X.EDIT_STRIP = False
print(("FAILS " + str(len(FAILS)) + ": " + ", ".join(FAILS)) if FAILS else "FAILS 0")
