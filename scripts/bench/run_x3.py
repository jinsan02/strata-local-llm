"""X3 — 저장소 코드를 읽고 고치는 탐색 평가 (pypa/packaging 고정 커밋).

두 방식:
  preload  : 필수 파일 + (의존하지 않는) 패딩 파일을 미리 넣고 길이를 맞춘다 (길이 효과). 첫 패치 실패 시 테스트 로그로 1회 보완.
  navigate : 파일을 넣지 않고 도구(list_files · grep · read_file)로 찾고 edit_file 로 고치게 한다 (탐색 확인, v2 = T-011).
             필수 파일을 실제로 읽었는지 도구 로그로 판정.

    python scripts/bench/run_x3.py --mode preload --inputs 0 16384 24320 --tasks dg_group_names marker_extras version_bump
    python scripts/bench/run_x3.py --mode navigate --tasks dg_group_names

참조 패치 · 비공개 테스트(configs/eval/x3-packaging/<task>/private)는 모델 입력과 작업 복사본에 들어가지 않는다.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_bench as rb  # noqa: E402

TASKS = rb.ROOT / "configs" / "eval" / "x3-packaging"
SRC = Path(r"C:\strata-lab\work\packaging-src")
RUNS = Path(r"C:\strata-lab\work\x3-runs")
PYX = r"C:\ProgramData\anaconda3\envs\x3_packaging\python.exe"
COMMIT = "6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc"
M0_SHA = "55983c5a75a1ab969824077b3bb3de4146e82a9234072b48ad4e8f92ad3fe9f1"
# 어떤 과제도 의존하지 않는 파일만, 고정 순서 (16K 패딩은 24K 패딩의 앞부분)
PAD_POOL = ["src/packaging/direct_url.py", "src/packaging/_elffile.py", "src/packaging/_musllinux.py",
            "src/packaging/_manylinux.py", "src/packaging/tags.py", "src/packaging/licenses/__init__.py",
            "src/packaging/pylock.py", "src/packaging/metadata.py", "src/packaging/ranges.py"]
LOG_LIMIT = 4000

FORMAT = """수정은 아래 형식의 편집 블록으로만 제시하라. 경로는 저장소 루트 기준이다.
SEARCH 부분은 현재 파일 내용과 공백까지 정확히 같아야 하고, 그 파일 안에서 한 번만 나와야 한다. 기존 테스트 파일은 고치지 마라.

### EDIT: src/packaging/example.py
<<<<<<< SEARCH
(바꿀 기존 코드)
=======
(새 코드)
>>>>>>> REPLACE

편집 블록은 여러 개 써도 된다. 설명은 짧게 하라."""

EDIT_RE = re.compile(r"### EDIT:\s*(\S+)\s*\n<<<<<<< SEARCH\n(.*?)\n?=======\n(.*?)\n?>>>>>>> REPLACE", re.S)


# ── 작업 복사본 · 편집 · 테스트 ─────────────────────────────────────────────
def fresh_copy(name: str) -> Path:
    d = RUNS / name
    if d.exists():
        shutil.rmtree(d, onerror=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
    subprocess.run(["git", "clone", "-q", "--no-checkout", str(SRC), str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "checkout", "-q", COMMIT], check=True)
    return d


LOOSE_RE = re.compile(r"<<<<<<< SEARCH\n(.*?)\n?=======\n(.*?)\n?>>>>>>> REPLACE", re.S)
PATH_RE = re.compile(r"((?:src|tests?|testing)/[\w./-]+\.py|[\w-]+/[\w./-]+\.py)")
LAST_FORMAT: dict = {}


def _dedent_pair(search: str, replace: str) -> tuple[str, str] | None:
    """SEARCH 의 모든 줄에 공통 들여쓰기가 있으면 둘 다 그만큼 뺀다 (모델이 블록 전체를 들여 쓴 경우)."""
    lines = [ln for ln in search.splitlines() if ln.strip()]
    if not lines:
        return None
    pad = min(len(ln) - len(ln.lstrip(" ")) for ln in lines)
    if pad == 0:
        return None
    strip = lambda s: "\n".join(ln[pad:] if ln[:pad] == " " * pad else ln.lstrip(" ") for ln in s.splitlines())  # noqa: E731
    return strip(search), strip(replace)


def apply_edits(root: Path, answer: str, candidates: list[str] | None = None,
                deny: tuple[str, ...] = ("tests",)) -> tuple[int, list[str]]:
    """(적용한 블록 수, 오류 목록). 형식 판정은 LAST_FORMAT 에 남긴다.

    엄격: `### EDIT: 경로` + SEARCH/REPLACE, SEARCH 가 파일과 정확히 일치.
    관대(기록만 다르게): 경로 줄이 없으면 블록 앞 300자에서 경로를 찾거나, 후보 파일 중 SEARCH 가 한 번만 맞는 파일에 적용.
    블록 전체를 들여 쓴 경우 공통 들여쓰기를 빼고 다시 맞춘다. (2026-11-18 X3 파일럿: 모델이 경로 줄을 빼고 4칸 들여 씀)
    """
    answer = answer or ""
    strict = [(m.start(), m.group(1), m.group(2), m.group(3)) for m in EDIT_RE.finditer(answer)]
    flags: set[str] = set()
    if strict:
        blocks = [(path, s, r) for _, path, s, r in strict]
    else:
        blocks = []
        for m in LOOSE_RE.finditer(answer):
            before = answer[max(0, m.start() - 300): m.start()]
            paths = PATH_RE.findall(before)
            blocks.append((paths[-1] if paths else None, m.group(1), m.group(2)))
        if blocks:
            flags.add("no_edit_header")
    errors, applied = [], 0
    for path, search, replace in blocks:
        targets = [path] if path else list(candidates or [])
        if not path:
            flags.add("path_inferred")
        done = False
        for tgt in targets:
            p = (root / tgt).resolve()
            if root.resolve() not in p.parents or any(d in Path(tgt).parts for d in deny):
                continue
            if not search.strip():
                if path:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(replace + "\n", encoding="utf-8", newline="\n")
                    applied += 1
                    done = True
                break
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")
            pairs = [(search, replace)]
            if (dd := _dedent_pair(search, replace)) is not None:
                pairs.append(dd)
            for k, (s, r) in enumerate(pairs):
                if text.count(s) == 1:
                    p.write_text(text.replace(s, r, 1), encoding="utf-8", newline="\n")
                    applied += 1
                    done = True
                    if k:
                        flags.add("dedented")
                    break
            if done:
                break
        if not done:
            where = path or f"경로 없음(후보 {len(targets)}개)"
            errors.append(f"{where}: SEARCH 가 파일 내용과 정확히 한 번 일치하지 않음")
    if not blocks:
        errors.append("편집 블록 없음")
    LAST_FORMAT.clear()
    LAST_FORMAT.update({"strict": bool(strict) and not flags and not errors, "flags": sorted(flags)})
    return applied, errors


def fmt_note() -> str:
    return f"format {'strict' if LAST_FORMAT.get('strict') else 'lenient:' + ','.join(LAST_FORMAT.get('flags') or ['-'])}"


def repair_feedback(errs: list[str], gr: dict | None) -> str:
    """보완 요청에 줄 내용: 적용 실패면 그 이유와 형식, 테스트 실패면 로그."""
    if gr is None:
        return ("편집을 하나도 적용하지 못했다.\n- " + "\n- ".join(errs) +
                "\n각 블록 위에 `### EDIT: <경로>` 줄을 쓰고, SEARCH 는 파일의 현재 내용을 들여쓰기까지 그대로 복사해야 한다.")
    head = ("일부 편집은 적용하지 못했다:\n- " + "\n- ".join(errs) + "\n\n") if errs else ""
    return head + "테스트 결과:\n" + gr["log"]


def run_pytest(root: Path, files: list[str]) -> dict:
    env = {**os.environ, "PYTHONPATH": str(root / "src")}
    t0 = time.perf_counter()
    try:
        r = subprocess.run([PYX, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "--tb=short", *files],
                           cwd=root, capture_output=True, text=True, timeout=900, env=env)
        out = r.stdout + r.stderr
        rc = r.returncode
    except subprocess.TimeoutExpired:
        out, rc = "pytest 시간 초과(900s)", 99
    ms = (time.perf_counter() - t0) * 1000
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", out)) else 0
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", out)) else 0
    errors = int(m.group(1)) if (m := re.search(r"(\d+) errors?", out)) else 0
    return {"rc": rc, "passed": passed, "failed": failed, "errors": errors, "ms": ms, "log": out}


def grade(root: Path, task_cfg: dict, hidden_total: int) -> dict:
    shutil.copy(TASKS / task_cfg["task"] / "private" / "test_x3_hidden.py", root / "tests" / "test_x3_hidden.py")
    h = run_pytest(root, ["tests/test_x3_hidden.py"])
    g = run_pytest(root, task_cfg["regress"])
    (root / "tests" / "test_x3_hidden.py").unlink()
    ok = h["rc"] == 0 and g["rc"] == 0
    # 로그는 실패한 쪽만, 비공개 테스트 소스 줄은 그대로 보여준다(일반 CI 로그와 같음)
    log = (h["log"] if h["rc"] else "") + ("\n--- 기존 테스트 ---\n" + g["log"] if g["rc"] else "")
    return {"ok": ok, "hidden": f"{h['passed']}/{hidden_total}", "regress_ok": g["rc"] == 0,
            "regress": f"{g['passed']} passed, {g['failed']} failed, {g['errors']} errors",
            "tools_ms": h["ms"] + g["ms"], "log": log[-LOG_LIMIT:]}


def error_type(applied: int, errs: list[str], gr: dict | None) -> str:
    if any("편집 블록 없음" in e for e in errs):
        return "no_edit"
    if errs and not applied:
        return "apply_fail"
    if gr is None:
        return "apply_fail"
    if gr["ok"]:
        return "pass" if not errs else "pass_partial_apply"
    if "error" in gr["log"].lower() and gr["hidden"].startswith("0/"):
        return "import_or_syntax"
    return "regress_fail" if not gr["regress_ok"] and gr["hidden"].split("/")[0] == gr["hidden"].split("/")[1] else "test_fail"


# ── 입력 만들기 (preload) ───────────────────────────────────────────────────
def file_block(root: Path, rel: str, limit: int | None = None) -> str:
    body = (root / rel).read_text(encoding="utf-8")
    if limit is not None and len(body) > limit:
        cut = body.rfind("\n", 0, limit)
        body = body[: max(cut, 0)] + "\n# ... (이 파일의 뒷부분 생략)\n"
    return f"### FILE: {rel}\n```python\n{body}\n```\n\n"


def build_preload(root: Path, task_cfg: dict, pad_chars: int) -> str:
    head = "다음은 작업 중인 저장소(pypa/packaging)의 파일들이다. 맨 아래의 과제를 수행하라.\n\n"
    pad, n = [], 0
    for rel in PAD_POOL:
        if n >= pad_chars:
            break
        blk = file_block(root, rel, limit=pad_chars - n)
        pad.append(blk)
        n += len(blk)
    req = "".join(file_block(root, rel) for rel in task_cfg["required_files"])
    task = (TASKS / task_cfg["task"] / "prompt.md").read_text(encoding="utf-8")
    return head + "".join(pad) + req + "### 과제\n" + task + "\n" + FORMAT


def count_tokens(base_url: str, api_key: str, prompt: str, timeout: float) -> int | None:
    return (rb.stream_chat(base_url, api_key, prompt, 1, timeout).get("usage") or {}).get("prompt_tokens")


# ── 도구 탐색 (navigate) ────────────────────────────────────────────────────
TOOLS = [
    {"type": "function", "function": {"name": "list_files", "description": "저장소 안 파일 목록 (glob 패턴, 최대 200개)",
     "parameters": {"type": "object", "properties": {"pattern": {"type": "string", "description": "예: src/packaging/*.py"}}, "required": ["pattern"]}}},
    {"type": "function", "function": {"name": "grep", "description": "정규식으로 파일 내용 검색 (최대 60줄)",
     "parameters": {"type": "object", "properties": {"pattern": {"type": "string"}, "path_glob": {"type": "string", "description": "예: src/**/*.py"}}, "required": ["pattern"]}}},
    {"type": "function", "function": {"name": "read_file", "description": "파일을 줄 번호와 함께 읽기 (한 번에 최대 400줄)",
     "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "start_line": {"type": "integer"}, "end_line": {"type": "integer"}}, "required": ["path"]}}},
]


# 2026-11-18 T-011: 읽기만 도구 · 쓰기는 텍스트 블록이던 혼합 방식에서 모델이 없는 'SEARCH' 도구를 텍스트로 불렀다.
# 실제 코딩 클라이언트처럼 쓰기도 도구로 한다(C안 = 편집 도구 + 가짜 호출 감지 후 1회 재요청). 마지막 답의 편집 블록도 계속 받는다.
EDIT_TOOL = {"type": "function", "function": {"name": "edit_file",
             "description": "파일 수정: old_string(현재 내용과 공백까지 정확히 같고 파일 안에서 한 번만 나오는 부분)을 new_string 으로 바꾼다. "
                            "old_string 을 빈 문자열로 주면 새 파일을 만든다. read_file 출력의 줄 번호는 old_string 에 넣지 않는다.",
             "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "저장소 루트 기준 경로"},
                            "old_string": {"type": "string"}, "new_string": {"type": "string"}},
                            "required": ["path", "old_string", "new_string"]}}}
NAV_TOOLS = TOOLS + [EDIT_TOOL]
NAV_FORMAT = ("수정은 edit_file 도구로 직접 하라(필요하면 여러 번). 사용할 수 있는 도구는 list_files · grep · read_file · edit_file 뿐이다. "
              "기존 테스트 파일은 고치지 마라. 수정을 마쳤으면 도구 없이 무엇을 바꿨는지 짧게 답하고 끝내라.")
FAKE_CALL_RE = re.compile(r"<tool_call>|<function=")


def edit_file(root: Path, args: dict, deny: tuple[str, ...]) -> tuple[bool, str]:
    path = args.get("path") or ""
    old, new = args.get("old_string"), args.get("new_string")
    if old is None or new is None:
        return False, "오류: path · old_string · new_string 이 모두 필요하다"
    p = (root / path).resolve()
    if not path or root.resolve() not in p.parents or ".git" in p.parts or any(d in Path(path).parts for d in deny):
        return False, f"오류: 수정할 수 없는 경로 {path} (테스트 파일 · 저장소 밖 금지)"
    if old == "":
        if p.exists():
            return False, f"오류: {path} 는 이미 있다. 바꿀 부분을 old_string 으로 줘라"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(new, encoding="utf-8", newline="\n")
        return True, f"새 파일 {path} 를 만들었다 ({len(new.splitlines())}줄)"
    if not p.is_file():
        return False, f"오류: {path} 파일이 없다"
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        hint = "read_file 로 현재 내용을 다시 확인하고 공백 · 들여쓰기까지 그대로 복사하라" if n == 0 else "앞뒤 줄을 더 넣어 한 곳만 맞게 하라"
        return False, f"오류: old_string 이 {path} 에서 {n}회 일치한다 (정확히 1회여야 함). {hint}"
    p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    return True, f"{path} 를 고쳤다 (-{len(old.splitlines())}줄 +{len(new.splitlines())}줄)"


def navigate_loop(root: Path, msgs: list, a, api_key: str, deny: tuple[str, ...], chat=None) -> dict:
    """도구 탐색 루프(X3 · SWE 공용). 편집은 edit_file 로 작업 트리에 바로 적용된다."""
    chat = chat or chat_once
    r = {"tool_log": [], "model_ms": 0.0, "tool_ms": 0.0, "out_tok": 0, "last_in": 0, "final": "", "status": "ok",
         "edit_ok": 0, "edit_fail": 0, "fake_calls": 0}
    fake_retry_left = 1
    for step in range(a.max_steps):
        force = step == a.max_steps - 1 or r["last_in"] > 24320 - 2048
        if force:
            msgs.append({"role": "user", "content": "이제 도구를 더 쓸 수 없다. 남은 수정이 있으면 편집 블록 형식으로, 없으면 바꾼 내용을 짧게 답하라.\n\n" + FORMAT})
        try:
            mt = max(1024, min(a.budget, a.ctx - r["last_in"] - 2048)) if r["last_in"] else a.budget
            data, ms = chat(a.base_url, api_key, msgs, mt, a.timeout, None if force else NAV_TOOLS)
        except Exception as ex:  # noqa: BLE001
            r["status"], r["final"] = "fail", f"요청 실패: {ex}"
            break
        r["model_ms"] += ms
        u = data.get("usage") or {}
        r["last_in"] = u.get("prompt_tokens") or r["last_in"]
        r["out_tok"] += u.get("completion_tokens") or 0
        msg = data["choices"][0]["message"]
        calls = msg.get("tool_calls") or []
        content = msg.get("content") or ""
        if not calls:
            if FAKE_CALL_RE.search(content) and not force:
                r["fake_calls"] += 1
                r["tool_log"].append({"step": step, "tool": "(text_tool_call)", "args": {}, "out_chars": len(content)})
                if fake_retry_left:
                    fake_retry_left -= 1
                    msgs.append({"role": "assistant", "content": content})
                    msgs.append({"role": "user", "content": "방금 답은 도구 호출이 아니라 텍스트로 처리됐다(없는 도구 이름이거나 형식 오류). "
                                 "사용할 수 있는 도구는 list_files · grep · read_file · edit_file 뿐이다. 파일 수정은 edit_file 로 하라."})
                    continue
            r["final"] = content
            break
        msgs.append({"role": "assistant", "content": content, "tool_calls": calls})
        for c in calls:
            fn = c["function"]["name"]
            try:
                args = json.loads(c["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            t0 = time.perf_counter()
            if fn == "edit_file":
                ok, out = edit_file(root, args, deny)
                r["edit_ok" if ok else "edit_fail"] += 1
                logged = {"path": args.get("path"), "ok": ok, "old_chars": len(args.get("old_string") or ""),
                          "new_chars": len(args.get("new_string") or "")}
            else:
                out, logged = run_tool(root, fn, args), args
            r["tool_ms"] += (time.perf_counter() - t0) * 1000
            r["tool_log"].append({"step": step, "tool": fn, "args": logged, "out_chars": len(out)})
            msgs.append({"role": "tool", "tool_call_id": c.get("id", ""), "content": out[:12000]})
    return r


def nav_apply_final(root: Path, r: dict, candidates: list[str], deny: tuple[str, ...]) -> tuple[int, list[str], str]:
    """edit_file 로 적용된 수 + 마지막 답의 편집 블록. (적용 수, 오류, 형식 메모)"""
    applied_b, errs = apply_edits(root, r["final"], candidates, deny=deny)
    note = fmt_note()
    if r["edit_ok"] and errs == ["편집 블록 없음"]:
        errs = []
    if r["edit_ok"]:
        note = "format tool" + (f"+{note}" if applied_b else "")
    return r["edit_ok"] + applied_b, errs, note


def _files(root: Path, pattern: str) -> list[str]:
    out = []
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix()
        if p.is_file() and not rel.startswith(".git/") and fnmatch.fnmatch(rel, pattern):
            out.append(rel)
    return sorted(out)


def run_tool(root: Path, name: str, args: dict) -> str:
    try:
        if name == "list_files":
            fs = _files(root, args.get("pattern") or "*")
            return "\n".join(fs[:200]) + (f"\n... ({len(fs)}개 중 200개)" if len(fs) > 200 else "") or "(없음)"
        if name == "grep":
            rx = re.compile(args["pattern"])
            hits = []
            for rel in _files(root, args.get("path_glob") or "src/**/*.py"):
                for i, line in enumerate((root / rel).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if rx.search(line):
                        hits.append(f"{rel}:{i}: {line[:200]}")
                        if len(hits) >= 60:
                            return "\n".join(hits) + "\n... (60줄에서 멈춤)"
            return "\n".join(hits) or "(일치 없음)"
        if name == "read_file":
            p = (root / args["path"]).resolve()
            if root.resolve() not in p.parents or ".git" in p.parts or not p.is_file():
                return "오류: 읽을 수 없는 경로"
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            s = max(1, int(args.get("start_line") or 1))
            e = min(len(lines), int(args.get("end_line") or s + 399), s + 399)
            return "\n".join(f"{i:5d}  {lines[i - 1]}" for i in range(s, e + 1)) + (f"\n... (전체 {len(lines)}줄)" if e < len(lines) else "")
        return f"오류: 알 수 없는 도구 {name}"
    except Exception as ex:  # noqa: BLE001
        return f"오류: {ex}"


def chat_once(base_url: str, api_key: str, messages: list, max_tokens: int, timeout: float, tools=None) -> tuple[dict, float]:
    body = {"model": "strata", "stream": False, "max_tokens": max_tokens, "messages": messages, **rb.SAMPLING, **rb.EXTRA_BODY}
    if tools:
        body["tools"] = tools
    req = urllib.request.Request(base_url.rstrip("/") + "/v1/chat/completions", data=rb.canon(body), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data, (time.perf_counter() - t0) * 1000


# ── 메인 ───────────────────────────────────────────────────────────────────
def base_row(a, rid: str, workload: str, env_sha: str, commit: str, dirty: str, cfg_sha: str, engine_commit: str) -> dict:
    return {"run_id": rid, "config_id": "X3", "phase": "eval", "origin": "local", "workload": workload, "model_id": "M0",
            "model_sha256": M0_SHA, "engine_commit": engine_commit, "settings_id": "S0", "ctx": a.ctx, "parallel": 1,
            "kv": "fp32", "mtp": "on", "thinking": "on", "cache_state": "cold", "git_commit": commit, "git_dirty": dirty,
            "config_sha256": cfg_sha, "env_sha256": env_sha}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["preload", "navigate"], required=True)
    ap.add_argument("--ctx", type=int, default=32768)
    ap.add_argument("--budget", type=int, default=8192)
    ap.add_argument("--inputs", type=int, nargs="+", default=[0, 16384, 24320], help="preload 목표 입력 토큰. 0 = 필수 파일만")
    ap.add_argument("--tasks", nargs="+", default=["dg_group_names", "marker_extras", "version_bump"])
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--prefix", default="x3")
    ap.add_argument("--max-steps", type=int, default=20)
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--timeout", type=float, default=1800)
    ap.add_argument("--chars-per-token", type=float, default=3.2)
    a = ap.parse_args()

    api_key = os.environ.get("STRATA_API_KEY", "strata-local")
    engine_dir = Path(r"C:\strata-lab\engine")
    server_cfg = json.loads((engine_dir / f"strata-qwen36-ctx{a.ctx}.json").read_text(encoding="utf-8"))
    engine_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=engine_dir, capture_output=True, text=True).stdout.strip()
    env = {"engine_commit": engine_commit, "engine_exe_sha256": rb.sha256_bytes(Path(server_cfg["exe"]).read_bytes()),
           "packaging_commit": COMMIT, "test_python": subprocess.run([PYX, "-V"], capture_output=True, text=True).stdout.strip()}
    env_sha = rb.sha256_bytes(rb.canon(env))
    commit, dirty = rb.git("rev-parse", "HEAD"), "1" if rb.git("status", "--porcelain") else "0"
    k = a.ctx // 1024

    for task in a.tasks:
        tcfg = json.loads((TASKS / task / "task.json").read_text(encoding="utf-8"))
        hidden_src = (TASKS / task / "private" / "test_x3_hidden.py").read_text(encoding="utf-8")
        hidden_total = len(re.findall(r"^def test_", hidden_src, flags=re.M))  # 매개변수화 전 함수 수 (아래에서 실제 수로 교체)
        probe = fresh_copy(f"{task}-count")
        shutil.copy(TASKS / task / "private" / "test_x3_hidden.py", probe / "tests" / "test_x3_hidden.py")
        c = subprocess.run([PYX, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "tests/test_x3_hidden.py"],
                           cwd=probe, capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(probe / "src")})
        if m := re.search(r"(\d+) tests? collected", c.stdout):
            hidden_total = int(m.group(1))

        conds = a.inputs if a.mode == "preload" else [0]
        for target in conds:
            for i in range(1, a.repeat + 1):
                tag = (f"in{round(target / 1024)}k" if target else "inreq") if a.mode == "preload" else "nav"
                run_name = f"{a.prefix}_m0_e0_s0_ctx{k}k_{tag}_{task}"
                run_dir = rb.ROOT / "experiments" / "runs" / run_name
                run_dir.mkdir(parents=True, exist_ok=True)
                root = fresh_copy(f"{run_name}_r{i}")
                if a.mode == "preload":
                    prompt = build_preload(root, tcfg, 0)
                    exact = count_tokens(a.base_url, api_key, prompt, a.timeout)
                    if target and exact and target > exact:
                        cpt = a.chars_per_token
                        for _ in range(3):
                            prompt = build_preload(root, tcfg, int((target - exact) * cpt))
                            got = count_tokens(a.base_url, api_key, prompt, a.timeout)
                            if not got or abs(got - target) <= max(64, target // 100):
                                break
                            cpt *= (target - exact) / max(1, got - exact) if got > exact else 1.5
                        exact = got
                    cfg = {"task": task, "mode": "preload", "commit": COMMIT, "prompt_sha256": rb.sha256_bytes(prompt.encode()),
                           "input_target": target, "prompt_tokens_exact": exact, "required_files": tcfg["required_files"],
                           "pad_pool": PAD_POOL, "budget": a.budget, "sampling": rb.SAMPLING, "server_config": server_cfg,
                           "thinking_cap": a.budget - min(max(512, a.budget // 4), a.budget // 2), "thinking_cap_source": "answer_room"}
                    cfg_sha = rb.sha256_bytes(rb.canon(cfg))
                    (run_dir / "config.json").write_bytes(rb.canon(cfg))
                    (run_dir / "env.json").write_bytes(rb.canon(env))
                    t_start = time.perf_counter()
                    # 1차 시도
                    rid1 = f"{run_name}_a1_r{i}"
                    row, res = rb.measure(a.base_url, api_key, prompt, a.budget, a.timeout, server_cfg,
                                          base_row(a, rid1, f"x3-preload-{task}", env_sha, commit, dirty, cfg_sha, engine_commit))
                    ans1 = res.get("answer", "") if row.get("status") == "ok" else ""
                    applied, errs = apply_edits(root, ans1, tcfg["required_files"])
                    fmt1 = fmt_note()
                    gr = grade(root, tcfg, hidden_total) if applied else None
                    et = error_type(applied, errs, gr)
                    row["tests_passed"] = gr["hidden"] if gr else f"0/{hidden_total}"
                    t_model1 = float(row.get("total_ms") or 0)
                    t_tools1 = gr["tools_ms"] if gr else 0.0
                    row["note"] = (f"{row.get('note', '')}; x3 attempt 1; edits {applied} ({'; '.join(errs) or 'ok'}); "
                                   f"regress {gr['regress'] if gr else 'NA'}; error_type {et}; {fmt1}; model_ms {t_model1:.0f}; tools_ms {t_tools1:.0f}")
                    rb.write_row(row)
                    (run_dir / f"answer_a1_r{i}.md").write_text(ans1, encoding="utf-8")
                    summary = {"run": run_name, "r": i, "a1": et, "a1_hidden": row["tests_passed"], "input": row.get("input_tokens")}
                    # 보완 1회
                    if et not in ("pass",):
                        log = repair_feedback(errs, gr)
                        msgs = [{"role": "user", "content": prompt}, {"role": "assistant", "content": ans1 or "(답 없음)"},
                                {"role": "user", "content": "위 편집을 적용하고 테스트를 돌린 결과다. 한 번만 고칠 기회가 있다. "
                                 "이미 적용된 상태의 파일을 기준으로 추가 편집 블록을 제시하라.\n\n```\n" + log + "\n```\n\n" + FORMAT}]
                        est_in = int(row.get("input_tokens") or exact or 0) + len(ans1) // 3 + len(log) // 3 + 400
                        budget2 = max(1024, min(a.budget, a.ctx - est_in - 256))
                        rid2 = f"{run_name}_a2_r{i}"
                        row2, res2 = rb.measure(a.base_url, api_key, msgs, budget2, a.timeout, server_cfg,
                                                base_row(a, rid2, f"x3-preload-{task}", env_sha, commit, dirty, cfg_sha, engine_commit),
                                                extra_cols=None)
                        ans2 = res2.get("answer", "") if row2.get("status") == "ok" else ""
                        applied2, errs2 = apply_edits(root, ans2, tcfg["required_files"])
                        fmt2 = fmt_note()
                        gr2 = grade(root, tcfg, hidden_total) if (applied2 or applied) else None
                        et2 = error_type(applied2 or applied, errs2, gr2)
                        row2["tests_passed"] = gr2["hidden"] if gr2 else f"0/{hidden_total}"
                        t_model2 = float(row2.get("total_ms") or 0)
                        t_tools2 = gr2["tools_ms"] if gr2 else 0.0
                        row2["note"] = (f"{row2.get('note', '')}; x3 attempt 2 (repair, budget {budget2}); edits {applied2} "
                                        f"({'; '.join(errs2) or 'ok'}); regress {gr2['regress'] if gr2 else 'NA'}; error_type {et2}; {fmt2}; "
                                        f"model_ms {t_model1 + t_model2:.0f}; tools_ms {t_tools1 + t_tools2:.0f}; "
                                        f"to_pass_ms {(time.perf_counter() - t_start) * 1000:.0f}" + ("" if et2 == "pass" else " (not passed)"))
                        rb.write_row(row2)
                        (run_dir / f"answer_a2_r{i}.md").write_text(ans2, encoding="utf-8")
                        (run_dir / f"log_a1_r{i}.txt").write_text(log, encoding="utf-8")
                        summary.update({"a2": et2, "a2_hidden": row2["tests_passed"], "budget2": budget2})
                    else:
                        summary["to_pass_ms"] = round((time.perf_counter() - t_start) * 1000)
                    print(json.dumps(summary, ensure_ascii=False), flush=True)
                else:
                    # navigate
                    task_txt = (TASKS / task / "prompt.md").read_text(encoding="utf-8")
                    sys_txt = ("너는 pypa/packaging 저장소(고정 커밋)에서 작업하는 코딩 에이전트다. 파일은 미리 주어지지 않는다. "
                               "list_files · grep · read_file 도구로 필요한 코드를 찾아 읽고, edit_file 도구로 직접 고쳐라.")
                    msgs = [{"role": "system", "content": sys_txt}, {"role": "user", "content": "### 과제\n" + task_txt + "\n\n" + NAV_FORMAT}]
                    cfg = {"task": task, "mode": "navigate", "harness": "nav-v2: edit_file + text-tool-call retry x1 (T-011)", "commit": COMMIT,
                           "tools": NAV_TOOLS, "max_steps": a.max_steps, "budget": a.budget, "sampling": rb.SAMPLING, "server_config": server_cfg}
                    cfg_sha = rb.sha256_bytes(rb.canon(cfg))
                    (run_dir / "config.json").write_bytes(rb.canon(cfg))
                    (run_dir / "env.json").write_bytes(rb.canon(env))
                    nr = navigate_loop(root, msgs, a, api_key, deny=("tests",))
                    tool_log, final, last_in = nr["tool_log"], nr["final"], nr["last_in"]
                    read = {t["args"].get("path") for t in tool_log if t["tool"] == "read_file"}
                    found = [f for f in tcfg["required_files"] if f in read]
                    applied, errs, fmtn = nav_apply_final(root, nr, sorted(p for p in read if p), ("tests",))
                    gr = grade(root, tcfg, hidden_total) if applied else None
                    et = error_type(applied, errs, gr)
                    rid = f"{run_name}_r{i}"
                    row = base_row(a, rid, f"x3-navigate-{task}", env_sha, commit, dirty, cfg_sha, engine_commit)
                    row.update({"ts_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "status": nr["status"], "input_tokens": last_in, "max_tokens": a.budget, "output_tokens": nr["out_tok"],
                                "answer_reached": 1 if (final.strip() or nr["edit_ok"]) else 0,
                                "tests_passed": gr["hidden"] if gr else f"0/{hidden_total}",
                                "total_ms": round(nr["model_ms"], 1), "note": (f"x3 navigate v2 (edit_file); steps {len(tool_log)} tool calls; required read "
                                f"{len(found)}/{len(tcfg['required_files'])} ({', '.join(found)}); edit_file ok {nr['edit_ok']} fail {nr['edit_fail']}; "
                                f"text_tool_calls {nr['fake_calls']}; edits {applied} ({'; '.join(errs) or 'ok'}); "
                                f"regress {gr['regress'] if gr else 'NA'}; error_type {et}; {fmtn}; model_ms {nr['model_ms']:.0f}; "
                                f"tool_exec_ms {nr['tool_ms']:.0f}; tests_ms {gr['tools_ms'] if gr else 0:.0f}; usage summed over turns")})
                    for col in rb.load_columns() if hasattr(rb, "load_columns") else []:
                        row.setdefault(col, "NA")
                    rb.write_row(row)
                    (run_dir / f"answer_r{i}.md").write_text(final, encoding="utf-8")
                    (run_dir / f"tools_r{i}.json").write_text(json.dumps(tool_log, ensure_ascii=False, indent=1), encoding="utf-8")
                    print(json.dumps({"run": rid, "tool_calls": len(tool_log), "required_read": f"{len(found)}/{len(tcfg['required_files'])}",
                                      "edit_ok": nr["edit_ok"], "edit_fail": nr["edit_fail"], "text_calls": nr["fake_calls"],
                                      "error_type": et, "hidden": row["tests_passed"], "last_input": last_in}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
