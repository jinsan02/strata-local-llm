"""11-22 노력치(--effort) 자체 점검: 서버 없이 resolve_effort 만 본다."""
import sys, types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_x3 as rx

def ns(**k):
    d = dict(ctx=65536, budget=8192, force_at=None, max_steps=None, effort="none"); d.update(k)
    return types.SimpleNamespace(**d)

ok = 0
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok += bool(cond)
    if not cond: sys.exit(1)

a = ns(ctx=32768); rx.resolve_effort(a); check("none 32K = 22272/20 (기존과 같음)", (a.force_at, a.max_steps) == (22272, 20))
a = ns(); rx.resolve_effort(a); check("none 64K = 55296/20 (x3k64h7 와 같음)", (a.force_at, a.max_steps) == (55296, 20))
exp = {"low": (22272, 12), "medium": (22272, 20), "high": (55296, 20), "xhigh": (55296, 30)}
for e, v in exp.items():
    a = ns(effort=e); rx.resolve_effort(a); check(f"{e} 64K = {v}", (a.force_at, a.max_steps) == v)
a = ns(ctx=32768, effort="high"); rx.resolve_effort(a); check("high 32K = 22528/20 (ctx 에 맞춰짐)", (a.force_at, a.max_steps) == (22528, 20))
for bad in (dict(force_at=30000), dict(max_steps=25)):
    try:
        rx.resolve_effort(ns(effort="medium", **bad)); check(f"충돌 거부 {bad}", False)
    except AssertionError:
        check(f"충돌 거부 {bad}", True)
a = ns(max_steps=7); rx.resolve_effort(a); check("none + --max-steps 7 그대로", a.max_steps == 7)
print(f"{ok}/10 통과")
