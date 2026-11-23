"""H8 게이트 자체 점검 (서버 · GPU 없이). python selftest_h8.py <bench_dir>
실제 지시문 6개 · 원본 packaging 소스 · 지난 실행의 작업 복사본(실패 · 통과)으로 검사가 맞게 걸리는지 본다.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent))
import h8_gate as h  # noqa: E402

NL = chr(10)
FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("ok   " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


# 1. 편집 검사
old = NL.join(["from .utils import canonicalize_name", "", "def f(x):", "    return canonicalize_name(x)", ""])
new = NL.join(["from .utils import canonicalize_name", "", "def f(x):", "    try:", "        return canonicalize_name(x)",
               "    except InvalidName as e:", "        raise ValueError(str(e))", ""])
check("정의 안 된 이름(InvalidName)을 잡는다", any("InvalidName" in p for p in h.lint_new("a.py", old, new)), str(h.lint_new("a.py", old, new)))
ann = NL.join(["from __future__ import annotations", "def g(x) -> frozenset[NormalizedName]:", "    y: NormalizedName = x", "    return y", ""])
check("주석 안의 이름은 잡지 않는다", h.lint_new("a.py", "", ann) == [], str(h.lint_new("a.py", "", ann)))
pre = NL.join(["def f():", "    return missing_one", ""])
check("편집 전에도 있던 문제는 다시 말하지 않는다", h.lint_new("a.py", pre, pre + "x = 1" + NL) == [])
dup = NL.join(["def _h(x):", "    return x", "", "def _h(x):", "    return x", ""])
check("같은 함수 두 번 정의를 잡는다", any("_h" in p for p in h.lint_new("a.py", "", dup)))
prop = NL.join(["class A:", "    @property", "    def v(self):", "        return 1", "    @v.setter", "    def v(self, x):", "        pass", ""])
check("property setter 는 중복으로 보지 않는다", h.lint_new("a.py", "", prop) == [], str(h.lint_new("a.py", "", prop)))
check("파이썬 파일이 아니면 검사하지 않는다", h.lint_new("a.txt", "", "x y z") == [])
check("편집 경고 문자열", "InvalidName" in h.edit_warning("a.py", old, new) and h.edit_warning("a.py", old, old) == "")
comp = NL.join(["def f(xs):", "    return [y for y in xs if y]", "", "g = lambda a, *b, **c: (a, b, c)", ""])
check("내포 · 람다 인자는 정의된 이름", h.lint_new("a.py", "", comp) == [], str(h.lint_new("a.py", "", comp)))
exc = NL.join(["try:", "    pass", "except ValueError as err:", "    print(err)", ""])
check("except as 이름은 정의된 이름", h.lint_new("a.py", "", exc) == [], str(h.lint_new("a.py", "", exc)))

# 2. 지시문 API 이름 · 원본 소스에서 '없는 것'
ROOT = Path(r"C:\strata-lab")
TASKS = ROOT / "configs" / "eval" / "x3-packaging"
SRC = ROOT / "work" / "packaging-src"
expect_missing = {
    "dg_group_names": {"InvalidGroupName"},
    "marker_extras": {"Marker.referenced_extras", "Requirement.marker_extras"},
    "specifier_bounds": {"bounds"},
    "version_bump": {"bump"},
    "tags_platform_filter": set(),
    "metadata_extra_dupes": set(),
}
if SRC.is_dir():
    texts = h._src_texts(SRC)
    check("원본 소스를 읽었다", len(texts) > 10, str(len(texts)))
    for task, exp in expect_missing.items():
        prompt = (TASKS / task / "prompt.md").read_text(encoding="utf-8")
        names = h.api_names(prompt)
        miss = set(h.api_missing(SRC, prompt, texts))
        check(f"{task}: 원본에서 없는 이름 = 새 API", miss == exp, f"names={names} missing={sorted(miss)}")
else:
    check("원본 소스 폴더", False, str(SRC))

# 3. 지난 실행 작업 복사본 (run_tests=False)
WS = ROOT / "work" / "x3-runs"
cases = [
    ("x3e1v3_m0_e1_s0_ctx64k_nav_dg_group_names_r5", "dg_group_names", "lint", "InvalidName"),
    ("x3k64h7_m0_e0_s0_ctx64k_nav_metadata_extra_dupes_r2", "metadata_extra_dupes", "lint", "_extract_extra_names"),
    ("x3k64h7_m0_e0_s0_ctx64k_nav_metadata_extra_dupes_r5", "metadata_extra_dupes", "unused", "_get_extra_values_from_marker"),
    ("x3e1v3_m0_e1_s0_ctx64k_nav_specifier_bounds_r1", "specifier_bounds", "api_missing", "bounds"),
]
for run, task, key, needle in cases:
    ws = WS / run
    if not ws.is_dir():
        check(f"{run} 작업 복사본", False, "없음")
        continue
    prompt = (TASKS / task / "prompt.md").read_text(encoding="utf-8")
    g = h.gate(ws, prompt, "", [], run_tests=False)
    check(f"{run}: {key} 에 {needle}", any(needle in x for x in g[key]), str({k: g[k] for k in ('lint', 'api_missing', 'unused')}))
for run, task in [("x3k64h7_m0_e0_s0_ctx64k_nav_dg_group_names_r1", "dg_group_names"),
                  ("x3k64h7_m0_e0_s0_ctx64k_nav_marker_extras_r1", "marker_extras"),
                  ("x3k64h7_m0_e0_s0_ctx64k_nav_version_bump_r1", "version_bump"),
                  ("x3k64h7_m0_e0_s0_ctx64k_nav_tags_platform_filter_r1", "tags_platform_filter")]:
    ws = WS / run
    if ws.is_dir():
        prompt = (TASKS / task / "prompt.md").read_text(encoding="utf-8")
        g = h.gate(ws, prompt, "", [], run_tests=False)
        check(f"{run} (통과 실행): 걸리는 것 없음", g["flags"] == 0, str({k: g[k] for k in ('lint', 'api_missing', 'unused')}))

# 4. 메시지
msg = h.checklist_message("과제 X", {"changed": ["src/a.py"], "lint": [], "api_missing": ["Foo"], "unused": [], "tests": "기존 테스트: 모두 통과"})
check("체크 턴 메시지에 지시문 · 이름 · 턴 수", "과제 X" in msg and "`Foo`" in msg and f"최대 {h.H8_EXTRA}턴" in msg and chr(92) not in msg)
check("알림 메시지", "3번" in h.notice_message(3))

print(("FAILS " + str(len(FAILS)) + ": " + ", ".join(FAILS)) if FAILS else "FAILS 0")
