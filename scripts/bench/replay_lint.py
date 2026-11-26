"""C1 재현: 지난 실행의 최종 작업 사본에서 모델이 바꾼 .py 에 '편집 뒤 진단'을 돌리면 무엇이 잡혔을지 센다.

진단 두 가지 (pyflakes 대신 표준 라이브러리, 설치 없음):
  S = 정적: 파싱 실패 · 정의 안 된 이름(symtable)
  I = import: 바뀐 src 모듈을 실제로 import (그 저장소의 conda 환경, PYTHONPATH=src)
기준 커밋(HEAD = setup)의 같은 파일에도 돌려, 모델이 새로 만든 문제만 센다. 숨은 테스트는 보지 않는다.

  python replay_lint.py <접두사...>     예: x3h9_ y9_ x3h9t_ y9t_ x3k64h7_
"""
import ast, builtins, collections, csv, json, os, re, subprocess, sys, symtable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.repo import error_type_of  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RUNS = str(ROOT / "work" / "x3-runs")
LEDGER = str(ROOT / "experiments" / "LEDGER.tsv")
PY = {"packaging": r"C:\ProgramData\anaconda3\envs\x3_packaging\python.exe",
      "flask": r"C:\ProgramData\anaconda3\envs\swe_flask_5014\python.exe"}
BUILTIN = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "__spec__", "__loader__", "__package__", "__path__",
                                "__builtins__", "__annotations__", "__dict__", "__module__", "__qualname__", "__class__"}


def git(root, *a):
    return subprocess.run(["git", "-C", root, "-c", "core.autocrlf=false", *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def static_issues(src: str, name: str) -> set[str]:
    try:
        ast.parse(src)
        top = symtable.symtable(src, name, "exec")
    except SyntaxError as e:
        return {f"syntax: {e.msg}"}
    if re.search(r"^\s*from\s+\S+\s+import\s+\*", src, re.M):
        return set()
    mod = {s.get_name() for s in top.get_symbols() if s.is_assigned() or s.is_imported() or s.is_parameter()}
    # 함수 안 global 선언으로 모듈 이름을 만드는 경우
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Global):
            mod |= set(n.names)
    out = set()

    def walk(t, depth):
        for s in t.get_symbols():
            n = s.get_name()
            if not s.is_referenced() or n in BUILTIN:
                continue
            if depth == 0:
                if not (s.is_assigned() or s.is_imported()) and n not in mod:
                    out.add(f"undefined name '{n}'")
            elif s.is_global() and n not in mod:
                out.add(f"undefined name '{n}'")
        for c in t.get_children():
            walk(c, depth + 1)
    walk(top, 0)
    return out


def import_issue(root: str, repo: str, rel: str) -> str | None:
    if not rel.startswith("src/") or not rel.endswith(".py"):
        return None
    mod = rel[4:-3].replace("/", ".")
    if mod.endswith(".__init__"):
        mod = mod[:-9]
    env = {**os.environ, "PYTHONPATH": os.path.join(root, "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    r = subprocess.run([PY[repo], "-c", f"import importlib; importlib.import_module({mod!r})"], cwd=root, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    if r.returncode == 0:
        return None
    last = [l for l in r.stderr.strip().splitlines() if l.strip()][-1:] or ["?"]
    return last[0][:160]


def outcome():
    o = {}
    for r in csv.DictReader(open(LEDGER, encoding="utf-8"), delimiter="\t"):
        et = error_type_of(r["note"])
        if et is not None:
            o[r["run_id"]] = et
    return o


def main(prefixes):
    out = outcome()
    rows = []
    for d in sorted(os.listdir(RUNS)):
        if not any(d.startswith(p) for p in prefixes):
            continue
        root = os.path.join(RUNS, d)
        if not os.path.isdir(os.path.join(root, ".git")):
            continue
        repo = "flask" if os.path.isdir(os.path.join(root, "src", "flask")) else "packaging"
        changed = [l[3:].strip().strip('"') for l in git(root, "status", "--porcelain", "-uall").splitlines()]
        changed = [c for c in changed if c.endswith(".py") and not c.startswith("tests/test_x3_hidden")]
        new_s, new_i = [], []
        for rel in changed:
            p = os.path.join(root, rel)
            if not os.path.exists(p):
                continue
            after = open(p, encoding="utf-8", errors="replace").read()
            before = git(root, "show", f"HEAD:{rel}")
            s = static_issues(after, rel) - (static_issues(before, rel) if before else set())
            new_s += [f"{rel}: {x}" for x in sorted(s)]
            ii = import_issue(root, repo, rel)
            if ii:
                new_i.append(f"{rel}: {ii}")
        rows.append({"run": d, "outcome": out.get(d, "?"), "changed_py": len(changed), "S": new_s, "I": new_i})
    # 요약
    agg = collections.defaultdict(collections.Counter)
    for r in rows:
        g = "pass" if r["outcome"] == "pass" else "fail"
        agg[g]["n"] += 1
        agg[g]["S"] += bool(r["S"])
        agg[g]["I"] += bool(r["I"])
        agg[g]["S|I"] += bool(r["S"] or r["I"])
    for g in ("fail", "pass"):
        print(g, dict(agg[g]))
    by = collections.Counter((r["outcome"], bool(r["S"] or r["I"])) for r in rows)
    print("outcome x flagged:", dict(by))
    for r in rows:
        if r["S"] or r["I"]:
            print(f"- {r['run']} [{r['outcome']}] S={r['S'][:3]} I={r['I'][:2]}")
    json.dump(rows, open(ROOT / "work" / "stage" / "replay_lint.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
