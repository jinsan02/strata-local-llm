"""H8 (11-23): 하네스 검사 게이트 + 요구사항 체크 턴. run_x3.navigate_loop 가 부른다(--h8 on 일 때만).

(1) 편집 때 검사: 편집 전 · 후 파일을 비교해 새로 생긴 '정의 안 된 이름' · '같은 이름 중복 정의' 를 경고로 돌려준다
    (문법 오류는 T1 이 편집을 거부한다; H8 은 T1 을 켠다).
(2) 끝 검사: 지시문의 API 이름(백틱 안의 CamelCase · 점 이름 · 이름(...))이 코드에 정의돼 있는지, 새로 만든 _헬퍼가
    호출되는지, 바뀐 파일의 (1) 문제, 공개(기존) 테스트 결과.
(3) 체크 턴 메시지: 지시문 원문 + 끝 검사 결과를 주고 항목마다 확인 · 수정하게 한다.
숨은 테스트 · 참조 패치는 쓰지 않는다(지시문 · 작업 복사본 · 공개 테스트만).
"""
from __future__ import annotations

import ast
import builtins
import os
import re
import subprocess
from pathlib import Path

BUILTINS = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "__all__", "__spec__", "__path__", "__builtins__",
                                 "__class__", "__annotations__", "__dict__", "__module__", "__qualname__"}
H8_EXTRA = 2                 # 체크 턴 + 고칠 턴: 도구를 쓰는 턴을 예산 밖에서 최대 2번 더 (11-23 사용자 결정)
H8_NOTICE_LEFT = 3           # 도구 턴이 이만큼 남으면 한 번 알린다
TEST_TIMEOUT = 300
NL = chr(10)


class _Names(ast.NodeVisitor):
    """읽힌 이름(주석 · 반환 타입 안은 빼고)과 묶인 이름."""

    def __init__(self) -> None:
        self.loads: set[str] = set()
        self.bound: set[str] = set()

    def visit_Name(self, n: ast.Name):
        (self.loads if isinstance(n.ctx, ast.Load) else self.bound).add(n.id)

    def visit_FunctionDef(self, n):
        self.bound.add(n.name)
        for d in n.decorator_list:
            self.visit(d)
        self._args(n.args)
        for s in n.body:
            self.visit(s)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _args(self, args: ast.arguments):
        for x in [*args.posonlyargs, *args.args, *args.kwonlyargs, *(a for a in (args.vararg, args.kwarg) if a)]:
            self.bound.add(x.arg)
        for d in [*args.defaults, *(d for d in args.kw_defaults if d is not None)]:
            self.visit(d)

    def visit_Lambda(self, n: ast.Lambda):
        self._args(n.args)
        self.visit(n.body)

    def visit_ClassDef(self, n):
        self.bound.add(n.name)
        for x in [*n.decorator_list, *n.bases, *(k.value for k in n.keywords)]:
            self.visit(x)
        for s in n.body:
            self.visit(s)

    def visit_AnnAssign(self, n: ast.AnnAssign):
        self.visit(n.target)
        if n.value is not None:
            self.visit(n.value)

    def visit_Import(self, n):
        for a in n.names:
            self.bound.add((a.asname or a.name).split(".")[0])

    visit_ImportFrom = visit_Import

    def visit_ExceptHandler(self, n):
        if n.name:
            self.bound.add(n.name)
        if n.type is not None:
            self.visit(n.type)
        for s in n.body:
            self.visit(s)

    def visit_Global(self, n):
        self.bound.update(n.names)

    visit_Nonlocal = visit_Global

    def visit_MatchAs(self, n):
        if n.name:
            self.bound.add(n.name)
        self.generic_visit(n)


def _undefined(tree: ast.AST) -> set[str]:
    v = _Names()
    v.visit(tree)
    return v.loads - v.bound - BUILTINS


def _dups(tree: ast.AST) -> set[str]:
    """같은 몸통(모듈 · 클래스) 안에서 두 번 이상 정의된 함수 · 클래스. property setter · overload 는 뺀다."""
    out: set[str] = set()

    def scan(body, prefix):
        seen: dict[str, int] = {}
        for n in body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                decos = getattr(n, "decorator_list", [])
                if any(isinstance(d, ast.Attribute) or (isinstance(d, ast.Name) and d.id == "overload") for d in decos):
                    continue
                seen[n.name] = seen.get(n.name, 0) + 1
                if isinstance(n, ast.ClassDef):
                    scan(n.body, prefix + n.name + ".")
        out.update(prefix + k for k, c in seen.items() if c > 1)

    scan(tree.body, "")
    return out


def lint_new(path: str, old_text: str | None, new_text: str) -> list[str]:
    """편집으로 새로 생긴 문제(편집 전에도 있던 것은 뺀다). 빈 목록 = 문제 없음."""
    if not path.endswith(".py"):
        return []
    try:
        nt = ast.parse(new_text)
    except SyntaxError as ex:
        return [f"문법 오류 줄 {ex.lineno}: {ex.msg}"]
    try:
        ot = ast.parse(old_text) if old_text else None
    except SyntaxError:
        ot = None
    und = _undefined(nt) - (_undefined(ot) if ot else set())
    dup = _dups(nt) - (_dups(ot) if ot else set())
    out = [f"정의되지 않은 이름 `{x}` (import · 정의가 빠졌을 수 있다)" for x in sorted(und)]
    out += [f"`{x}` 가 같은 곳에서 두 번 정의됐다 (뒤의 것이 앞의 것을 덮는다)" for x in sorted(dup)]
    return out


def edit_warning(path: str, old_text: str | None, new_text: str) -> str:
    probs = lint_new(path, old_text, new_text)
    if not probs:
        return ""
    return NL + "[하네스 검사] 이 편집 뒤 " + path + " 에서: " + "; ".join(probs) + ". 의도한 것이 아니면 고쳐라."


def _git(root: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def changed_py(root: Path) -> list[str]:
    files = _git(root, "diff", "--name-only", "HEAD").split() + _git(root, "ls-files", "--others", "--exclude-standard").split()
    return sorted({f for f in files if f.endswith(".py") and not f.startswith("tests/")})


def _src_texts(root: Path) -> dict[str, str]:
    out = {}
    for p in (root / "src").rglob("*.py"):
        try:
            out[p.relative_to(root).as_posix()] = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass
    return out


API_CHUNK = re.compile(r"`([^`]+)`")
API_HEAD = re.compile(r"^([A-Za-z_][\w.]*)(\(|$)")


def api_names(prompt: str) -> list[str]:
    """지시문 백틱 안에서 검사할 이름: 점이 든 이름, 이름( 으로 시작, CamelCase(대문자 둘 이상, 예: InvalidGroupName).
    `Name` · `None` 같은 한 단어는 뺀다. 점 이름의 마지막 부분과 같은 맨 이름(`bump()` 와 `Version.bump`)은 하나만 남긴다."""
    out: list[str] = []
    for chunk in API_CHUNK.findall(prompt):
        m = API_HEAD.match(chunk.strip())
        if not m:
            continue
        name, paren = m.group(1).rstrip("."), m.group(2) == "("
        last = name.split(".")[-1]
        camel = last[:1].isupper() and any(ch.islower() for ch in last) and sum(ch.isupper() for ch in last) >= 2
        if ("." in name or paren or camel) and name not in out:
            out.append(name)
    dotted_last = {n.split(".")[-1] for n in out if "." in n and not n.startswith("packaging.")}
    return [n for n in out if "." in n or n not in dotted_last]


def _defined(text: str, name: str) -> bool:
    """def · class 정의, 또는 0열의 모듈 수준 대입(상수). 함수 안 지역 변수 대입은 정의로 보지 않는다."""
    e = re.escape(name)
    return bool(re.search(r"\b(def|class)\s+" + e + r"\b", text) or re.search(r"^" + e + r"\s*(:[^=]+)?=", text, re.M))


def _member_defined(texts: dict[str, str], cls: str, member: str) -> bool | None:
    """클래스 cls 안에 member(메서드 · property · 클래스 변수)가 있으면 True, 클래스가 있는데 없으면 False, 클래스가 없으면 None."""
    found = False
    for t in texts.values():
        if ("class " + cls) not in t:
            continue
        try:
            tree = ast.parse(t)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.ClassDef) and n.name == cls:
                found = True
                for b in n.body:
                    if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)) and b.name == member:
                        return True
                    if isinstance(b, (ast.Assign, ast.AnnAssign)):
                        tg = b.targets if isinstance(b, ast.Assign) else [b.target]
                        if any(isinstance(x, ast.Name) and x.id == member for x in tg):
                            return True
    return False if found else None


def api_missing(root: Path, prompt: str, texts: dict[str, str] | None = None) -> list[str]:
    texts = texts if texts is not None else _src_texts(root)
    blob = NL.join(texts.values())
    missing = []
    for name in api_names(prompt):
        parts = name.split(".")
        if parts[0] == "packaging":   # 모듈 경로(packaging.x.y): 모듈 파일이 있거나, 부모 모듈에 마지막 이름이 정의돼 있으면 있음
            as_mod = "src/" + "/".join(parts) + ".py"
            as_pkg = "src/" + "/".join(parts) + "/__init__.py"
            parent = "src/" + "/".join(parts[:-1]) + ".py"
            if as_mod in texts or as_pkg in texts or (parent in texts and _defined(texts[parent], parts[-1])):
                continue
            missing.append(name)
            continue
        last = parts[-1]
        if last in BUILTINS:
            continue
        if len(parts) >= 2:
            md = _member_defined(texts, parts[-2], last)
            if md is True or (md is None and _defined(blob, last)):
                continue
            missing.append(name)
            continue
        if _defined(blob, last):
            continue
        missing.append(name)
    return missing


def unused_helpers(root: Path, changed: list[str], texts: dict[str, str] | None = None) -> list[str]:
    """바뀐 파일에 새로 생긴 모듈 수준 _함수 중 자기 몸통 밖 어디에서도 쓰이지 않는 것."""
    texts = texts if texts is not None else _src_texts(root)
    out = []
    for rel in changed:
        new = texts.get(rel)
        if new is None:
            continue
        old = _git(root, "show", f"HEAD:{rel}")
        try:
            nt = ast.parse(new)
            old_names = {n.name for n in ast.parse(old).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))} if old else set()
        except SyntaxError:
            continue
        lines = new.splitlines()
        for n in nt.body:
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) or not n.name.startswith("_") or n.name in old_names:
                continue
            pat = re.compile(r"\b" + re.escape(n.name) + r"\b")
            outside = NL.join(lines[: n.lineno - 1] + lines[(n.end_lineno or n.lineno):])
            uses = len(pat.findall(outside)) + sum(len(pat.findall(t)) for r2, t in texts.items() if r2 != rel)
            if uses == 0:
                out.append(f"{rel}:{n.name}")
    return out


def visible_tests(root: Path, pyx: str, files: list[str]) -> str:
    env = {**os.environ, "PYTHONPATH": str(root / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        r = subprocess.run([pyx, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "--tb=line", *files],
                           cwd=root, capture_output=True, text=True, errors="replace", timeout=TEST_TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return f"기존 테스트: {TEST_TIMEOUT}초 안에 끝나지 않음"
    out = (r.stdout or "") + (r.stderr or "")
    summ = next((ln.strip("= ") for ln in reversed(out.splitlines()) if re.search(r"\d+ (passed|failed|errors?)\b", ln)), "(요약 없음)")
    if r.returncode == 0:
        return f"기존 테스트: 모두 통과 ({summ})"
    fails = [ln for ln in out.splitlines() if ln.startswith(("FAILED", "ERROR")) or re.match(r"^\S+\.py:\d+: ", ln)][:6]
    return f"기존 테스트: 실패 있음 ({summ})" + NL + NL.join(fails)


def gate(root: Path, prompt: str, pyx: str, regress: list[str], run_tests: bool = True) -> dict:
    texts = _src_texts(root)
    changed = changed_py(root)
    lint = []
    for rel in changed:
        p = root / rel
        new = texts.get(rel) or (p.read_text(encoding="utf-8") if p.is_file() else None)
        if new is None:
            continue
        lint += [f"{rel}: {x}" for x in lint_new(rel, _git(root, "show", f"HEAD:{rel}") or None, new)]
    miss = api_missing(root, prompt, texts)
    unused = unused_helpers(root, changed, texts)
    if not run_tests:
        tests = "기존 테스트: (오프라인 점검이라 돌리지 않음)"
    else:
        tests = visible_tests(root, pyx, regress) if changed else "기존 테스트: 바뀐 파일이 없어 돌리지 않음"
    bad_tests = not any(s in tests for s in ("모두 통과", "돌리지 않음"))
    return {"changed": changed, "lint": lint, "api_missing": miss, "unused": unused, "tests": tests,
            "flags": len(lint) + len(miss) + len(unused) + int(bad_tests)}


def checklist_message(prompt: str, g: dict, extra: int = H8_EXTRA) -> str:
    rows = [
        "바뀐 파일: " + (", ".join(g["changed"]) if g["changed"] else "없음 (아직 아무것도 고치지 않았다)"),
        "코드 검사: " + ("; ".join(g["lint"]) if g["lint"] else "문제 없음"),
        "지시문에 나온 이름 중 코드에 정의가 없는 것: " + (", ".join(f"`{x}`" for x in g["api_missing"]) if g["api_missing"] else "없음"),
        "새로 만들었지만 어디서도 부르지 않는 함수: " + (", ".join(g["unused"]) if g["unused"] else "없음"),
        g["tests"],
    ]
    return ("[하네스 점검] 끝내기 전에 과제 요구사항을 하나씩 확인하라." + NL + NL + "자동 검사 결과:" + NL + "- " + (NL + "- ").join(rows)
            + NL + NL + "과제 지시문(다시):" + NL + prompt.strip() + NL + NL
            + "지시문의 요구사항(항목 · 조건 · 예외 · 예시)마다 이미 반영했는지 '파일:줄' 로 짧게 확인하라. 빠졌거나 틀린 것, 위 검사에서 나온 문제가 있으면 "
            + f"edit_file 로 고쳐라. 도구는 최대 {extra}턴 더 쓸 수 있다. 모두 반영했으면 도구 없이 바꾼 내용을 짧게 답하라.")


def notice_message(left: int) -> str:
    return NL + NL + f"[하네스 알림] 도구를 쓸 수 있는 턴이 {left}번 남았다. 아직 하지 않은 수정이 있으면 지금 edit_file 로 하라."
