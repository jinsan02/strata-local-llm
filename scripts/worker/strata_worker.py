"""로컬 LLM 워커 — 지휘자(Claude Code · Codex 등)가 넘긴 작은 코딩 작업 하나를 STRATA 로 처리하고 diff 를 돌려준다.

지휘자가 큰 일을 X3 크기 티켓(파일 1~3개, 수십 줄, 명세 · 테스트 기준이 분명한 것)으로 쪼개 넘기는 용도다.
하네스는 X3 의 탐색 루프(scripts/bench/run_x3.py navigate_loop)를 그대로 쓴다. 설정은 configs/worker.json
(H3 · 채택 확인 뒤 채택안으로 바꾼다).

흐름: 서버 확인 → 대상 저장소의 커밋을 별도 작업 트리로 꺼냄(원본 작업 트리는 건드리지 않음) → 탐색 · 수정 루프 →
(test_cmd 가 있으면) 테스트 → 실패하면 다시 시도 → diff · 테스트 결과 · 통계 반환. 원시 기록은
work/worker/logs/<id>.json (git 제외).
다시 시도(11-22, docs/effort-20261122.md): retry=escalate 이면 노력치를 한 단계 올려 처음부터(실패한 변경은 버림),
retry=repair 이면 같은 노력치로 이전 diff · 테스트 로그를 주고 1회 보완(예전 방식).

    python scripts/worker/strata_worker.py --repo C:\\path\\to\\repo --task "..." [--files a.py b.py] [--test-cmd "..."]
    python scripts/worker/strata_worker.py --status

주의: 원본 저장소의 커밋되지 않은 변경은 작업 트리에 들어가지 않는다(지휘자가 먼저 커밋하거나 push 한다).
서버는 단일 슬롯이라 한 번에 한 작업만 돈다(잠금 파일).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import types
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parents[1]
sys.path.insert(0, str(LAB / "scripts" / "bench"))
import run_x3 as x3  # noqa: E402

CFG_PATH = LAB / "configs" / "worker.json"
WORK = LAB / "work" / "worker"
LOGS = WORK / "logs"
LOCK = WORK / "busy.lock"
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache", "dist", "build", ".tox"}
LOG_TAIL = 4000
DIFF_LIMIT = 60000

DEFAULTS = {"harness": "H0", "tool_out": "chars", "reasoning_echo": "none", "final_turn": "none", "max_steps": 20,
            "ctx": 32768, "budget": 8192, "timeout": 1800, "test_timeout": 600, "repair": 1,
            # 11-22: 채택 하네스 · 노력치(docs/effort-20261122.md). 파일에 없으면 예전과 같은 값
            "sampling": "card-general", "edit_apply": "strict", "effort": None, "max_effort": "xhigh", "retry": "repair",
            "syntax_check": "off", "code_tools": "off", "edit_strip": "off"}


def load_cfg(override: dict | None = None) -> dict:
    cfg = dict(DEFAULTS)
    if CFG_PATH.is_file():
        cfg.update(json.loads(CFG_PATH.read_text(encoding="utf-8")))
    cfg.update(override or {})
    return cfg


def server_ctx(base: str) -> int | None:
    """서버 /health 의 max_context (노력치 high · xhigh 문턱을 실제 서버 크기에 맞춘다). 모르면 None."""
    try:
        with urllib.request.urlopen(base + "/health", timeout=5) as r:
            return int(json.loads(r.read().decode("utf-8")).get("max_context") or 0) or None
    except Exception:  # noqa: BLE001
        return None


def effort_ladder(start: str | None, cfg: dict, test_cmd: str | None, repair: bool | None) -> list:
    """시도마다 쓸 노력치. 재시도는 테스트가 있을 때만. escalate = 한 단계씩 올려 처음부터, repair = 같은 노력치로 보완(예전 방식)."""
    retry_on = bool(test_cmd) and (repair if repair is not None else bool(int(cfg["repair"])))
    if not retry_on:
        return [start]
    if cfg["retry"] == "escalate" and start is not None:
        lv = list(x3.EFFORT_LEVELS)
        top = max(lv.index(start), lv.index(cfg["max_effort"]))
        return lv[lv.index(start): top + 1] if top > lv.index(start) else [start]
    return [start] * (1 + max(1, int(cfg["repair"])))


def api_key() -> str:
    k = os.environ.get("STRATA_API_KEY", "")
    if not k:
        f = LAB / ".secrets" / "strata-api-key.txt"
        k = f.read_text(encoding="utf-8").strip() if f.is_file() else "strata-local"
    return k


def find_server(key: str) -> tuple[str | None, str]:
    """STRATA_BASE_URL → 루프백 → Tailscale 주소 순서로 /v1/models 를 확인한다 (serve-ctx -Host_ 로 띄웠으면 루프백이 안 열림)."""
    cands = [os.environ.get("STRATA_BASE_URL", ""), "http://127.0.0.1:8080"]
    last = ""
    for base in [c.rstrip("/") for c in cands if c]:
        try:
            req = urllib.request.Request(base + "/v1/models", headers={"Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    return base, "ok"
        except Exception as ex:  # noqa: BLE001
            last = f"{base}: {ex}"
    return None, last


BENCH_RE = re.compile(r"night-chain|matrix-[a-z0-9]+\.ps1|run_(x3|swe|bench|coding)\.py", re.I)


def measuring() -> str | None:
    """측정 체인 · 러너가 떠 있으면 그 명령줄 일부. 같은 GPU · 서버를 쓰므로 워커는 그동안 돌지 않는다."""
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='powershell.exe' or Name='python.exe'\" | "
          "ForEach-Object { $_.CommandLine }")
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=30).stdout
    except Exception:  # noqa: BLE001
        return None
    for line in out.splitlines():
        if BENCH_RE.search(line) and "strata_worker" not in line:
            return line.strip()[:160]
    return None


# ── 범용 저장소용 도구 조정 (X3 도구는 packaging 기준 기본값이라 바꿔 끼운다) ─────────────
def _files(root: Path, pattern: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            rel = (Path(dirpath) / fn).relative_to(root).as_posix()
            if x3.fnmatch.fnmatch(rel, pattern):
                out.append(rel)
    return sorted(out)


def _with_default_glob(fn):
    def wrapped(root, name, args):
        if name == "grep" and isinstance(args, dict) and not args.get("path_glob"):
            args = {**args, "path_glob": "**/*"}
        return fn(root, name, args)
    return wrapped


x3._files = _files
x3.run_tool = _with_default_glob(x3.run_tool)
x3.run_tool_paged = _with_default_glob(x3.run_tool_paged)


# ── 작업 트리 ─────────────────────────────────────────────────────────────
def git(cwd: Path, *a, check=True) -> str:
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a)}: {r.stderr.strip()[:400]}")
    return r.stdout


def make_tree(repo: str, ref: str | None, wid: str) -> tuple[Path, str, str]:
    """(작업 트리, 기준 커밋, 방식). 로컬 경로면 git worktree, URL 이면 clone."""
    dst = WORK / wid
    if re.match(r"^(https?://|git@|ssh://)", repo):
        git(WORK, "clone", "-q", "--filter=blob:none", repo, str(dst))
        if ref:
            git(dst, "checkout", "-q", "--detach", ref)
        kind = "clone"
    else:
        src = Path(repo).resolve()
        if not (src / ".git").exists():
            raise RuntimeError(f"git 저장소가 아니다: {src}")
        git(src, "worktree", "add", "-q", "--detach", str(dst), ref or "HEAD")
        kind = "worktree"
    return dst, git(dst, "rev-parse", "HEAD").strip(), kind


def drop_tree(worker_id: str) -> str:
    dst = WORK / worker_id
    if not dst.exists():
        return "없음"
    common = git(dst, "rev-parse", "--git-common-dir", check=False).strip()
    src = Path(common).resolve().parent if common and Path(common).is_absolute() else None
    if src and (dst / ".git").is_file():
        git(src, "worktree", "remove", "--force", str(dst), check=False)
    if dst.exists():
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(dst)], capture_output=True)
    return "삭제" if not dst.exists() else "일부 남음"


def diff_of(root: Path) -> tuple[str, str]:
    spec = ["--", ".", ":(exclude,glob)**/__pycache__/**", ":(exclude,glob)**/*.pyc", ":(exclude,glob)**/.pytest_cache/**"]
    git(root, "add", "-A", "-N", *spec)   # 새 파일도 diff 에 나오게 (스테이징은 하지 않음). 캐시 파일은 뺀다
    return git(root, "diff", "--no-color", *spec), git(root, "diff", "--stat", "--no-color", *spec).strip()


def run_tests(root: Path, cmd: str, timeout: int) -> dict:
    t0 = time.perf_counter()
    try:
        # 바이트코드를 쓰지 않는다: 보완 시도에서 같은 크기 · 같은 초에 고친 소스를 옛 .pyc 가 가리는 일을 막는다 (selftest 2 에서 확인)
        r = subprocess.run(cmd, cwd=root, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        out, code = (r.stdout or "") + (r.stderr or ""), r.returncode
    except subprocess.TimeoutExpired as ex:
        out, code = f"(시간 초과 {timeout}초)\n" + str(ex.stdout or "")[-LOG_TAIL:], None
    return {"cmd": cmd, "exit_code": code, "passed": code == 0, "ms": round((time.perf_counter() - t0) * 1000),
            "tail": out[-LOG_TAIL:], "_full": out}


# ── 프롬프트 ──────────────────────────────────────────────────────────────
def build_msgs(repo_name: str, task: str, files: list[str], test_cmd: str | None, extra: str = "", code_tools: bool = False) -> list:
    read_tools = "list_files · grep · read_file" + (" · outline · read_symbol" if code_tools else "")
    sys_txt = (f"너는 로컬 코딩 워커다. 저장소 {repo_name} 의 작업 트리에서 주어진 작업 하나만 한다. 파일은 미리 주어지지 않는다. "
               f"{read_tools} 도구로 필요한 코드를 찾아 읽고, edit_file 도구로 직접 고쳐라. "
               "작업에 필요한 파일만 고치고, 관계없는 정리 · 리팩터링 · 서식 변경은 하지 마라.")
    parts = ["### 작업\n" + task.strip()]
    if files:
        parts.append("### 먼저 볼 파일\n" + "\n".join(f"- {f}" for f in files))
    if test_cmd:
        parts.append(f"### 확인\n수정이 끝나면 하네스가 `{test_cmd}` 를 돌려 확인한다. 너는 명령을 실행할 수 없다.")
    if extra:
        parts.append(extra)
    parts.append(f"수정은 edit_file 도구로 직접 하라(필요하면 여러 번). 사용할 수 있는 도구는 {read_tools} · edit_file 뿐이다. "
                 "수정을 마쳤으면 도구 없이 무엇을 바꿨는지 짧게 답하고 끝내라.")
    if code_tools:
        parts.append(x3.CODE_TOOLS_NOTE)
    return [{"role": "system", "content": sys_txt}, {"role": "user", "content": "\n\n".join(parts)}]


def loop_args(cfg: dict, base: str, max_steps: int | None, ctx: int | None = None, effort: str | None = None) -> types.SimpleNamespace:
    """effort 가 있으면 run_x3.resolve_effort 로 문턱 · 호출 상한을 정한다(X3 측정과 같은 규칙). max_steps 를 직접 주면 호출 상한만 덮는다."""
    a = types.SimpleNamespace(base_url=base, ctx=ctx or cfg["ctx"], budget=cfg["budget"], timeout=cfg["timeout"],
                              max_steps=None, force_at=None, effort=effort or "none", tool_out=cfg["tool_out"],
                              reasoning_echo=cfg["reasoning_echo"], final_turn=cfg["final_turn"], code_tools=cfg["code_tools"])
    if effort is None:
        a.max_steps = cfg["max_steps"]
        a.force_at = a.ctx - cfg["budget"] - 2048        # 예전 워커와 같음 (노력치를 안 쓸 때)
    else:
        x3.resolve_effort(a)
    if max_steps:
        a.max_steps = max_steps
    return a


def apply_harness(cfg: dict) -> None:
    """X3 모듈 전역 설정을 워커 설정에 맞춘다(샘플링 · 편집 적용 · H9 · 문법 검사)."""
    x3.apply_sampling(cfg["sampling"])
    x3.EDIT_APPLY = cfg["edit_apply"]
    x3.SYNTAX_CHECK = cfg["syntax_check"] == "on"
    x3.EDIT_STRIP = cfg["edit_strip"] == "on" and cfg["edit_apply"] == "lenient"   # 11-23 H9: lenient 마지막 단계로 줄마다 앞뒤 공백 무시 한 곳 일치


def reset_tree(root: Path) -> None:
    """자동 올리기: 실패한 시도의 변경을 버리고 기준 커밋 상태로 (처음부터 새로)."""
    git(root, "checkout", "-q", "--", ".")
    git(root, "clean", "-fdq")


def stats(nr: dict) -> dict:
    keys = ("model_ms", "tool_ms", "out_tok", "edit_ok", "edit_fail", "fake_calls", "bad_json", "tool_errors", "forced_turns", "status")
    s = {k: (round(nr[k]) if isinstance(nr.get(k), float) else nr.get(k)) for k in keys}
    s["model_calls"] = len(nr["turns"])
    s["max_in"] = max((t.get("prompt_tokens") or 0 for t in nr["turns"]), default=0)
    return s


# ── 본체 ──────────────────────────────────────────────────────────────────
class Busy(RuntimeError):
    pass


def _lock():
    WORK.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        info = LOCK.read_text(encoding="utf-8", errors="replace") if LOCK.exists() else ""
        pid = int(info.split()[0]) if info.split() and info.split()[0].isdigit() else None
        alive = pid is not None and subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True,
                                                   text=True).stdout.find(str(pid)) >= 0
        if alive:
            raise Busy(f"다른 작업이 돌고 있다 ({info.strip()})")
        LOCK.unlink(missing_ok=True)
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, f"{os.getpid()} {time.strftime('%Y-%m-%d %H:%M:%S')}".encode())
    os.close(fd)


def delegate(task: str, repo: str, ref: str | None = None, files: list[str] | None = None, test_cmd: str | None = None,
             max_steps: int | None = None, repair: bool | None = None, keep_worktree: bool = True, chat=None, counter=None,
             effort: str | None = None, cfg_override: dict | None = None) -> dict:
    cfg = load_cfg(cfg_override)
    key = api_key()
    files = files or []
    effort = effort or cfg.get("effort")
    if effort is not None and effort not in x3.EFFORT_LEVELS:
        return {"status": "error", "error": f"effort 는 {', '.join(x3.EFFORT_LEVELS)} 중 하나 ({effort!r})"}
    ctx = None
    if chat is None:
        base, why = find_server(key)
        if not base:
            return {"status": "server_down", "error": f"STRATA 서버에 닿지 않는다 ({why}). 본체에서 "
                    f"`powershell -File C:\\strata-lab\\scripts\\serve-ctx.ps1 -Context {cfg['ctx']}` 로 띄운다."}
        bench = measuring()
        if bench:
            return {"status": "busy", "error": f"측정 체인이 돌고 있어 워커를 쓰지 않는다(측정값이 흔들림): {bench}"}
        ctx = server_ctx(base)
    else:
        base = "http://fake"
    apply_harness(cfg)
    try:
        _lock()
    except Busy as ex:
        return {"status": "busy", "error": str(ex)}
    wid = time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]
    t_wall = time.perf_counter()
    rec = {"worker_id": wid, "repo": repo, "ref": ref, "task": task, "files": files, "test_cmd": test_cmd, "cfg": cfg, "attempts": []}
    try:
        root, base_commit, kind = make_tree(repo, ref, wid)
        rec.update(base_commit=base_commit, tree_kind=kind)
        name = Path(repo.rstrip("/\\")).name.removesuffix(".git")
        code_tools = cfg["code_tools"] == "on"
        msgs = build_msgs(name, task, files, test_cmd, code_tools=code_tools)
        ladder = effort_ladder(effort, cfg, test_cmd, repair)
        escalate = cfg["retry"] == "escalate" and effort is not None
        rec.update(effort=effort, ladder=ladder, server_ctx=ctx)
        test = None
        for n, lvl in enumerate(ladder):
            if n and escalate:   # 자동 올리기: 실패한 시도는 버리고 한 단계 높은 노력치로 처음부터
                reset_tree(root)
                msgs = build_msgs(name, task, files, test_cmd, code_tools=code_tools)
            a = loop_args(cfg, base, max_steps, ctx, lvl)
            nr = x3.navigate_loop(root, msgs, a, key, deny=(), chat=chat, counter=counter)
            read = x3.nav_read_ok(nr["tool_log"])
            applied, errs, fmt = x3.nav_apply_final(root, nr, sorted(p for p in read if p), ())
            att = {"n": n + 1, "effort": lvl, "force_at": a.force_at, "max_steps": a.max_steps, "ctx": a.ctx,
                   "stats": stats(nr), "applied": applied, "apply_errors": errs, "format": fmt,
                   "final": nr["final"][-2000:], "turns": nr["turns"], "tool_log": nr["tool_log"]}
            if test_cmd:
                test = run_tests(root, test_cmd, cfg["test_timeout"])
                att["test"] = {k: v for k, v in test.items() if k != "_full"}
            rec["attempts"].append(att)
            if not test_cmd or test["passed"] or n + 1 >= len(ladder) or nr["status"] != "ok":
                break
            if not escalate:
                cur, _ = diff_of(root)
                msgs = build_msgs(name, task, files, test_cmd, code_tools=code_tools, extra=(
                    "### 이전 시도\n이미 아래 변경이 작업 트리에 적용돼 있다. 테스트가 실패했다. 한 번만 더 고칠 기회가 있다.\n\n"
                    f"```diff\n{cur[-6000:]}\n```\n\n테스트 출력 끝부분:\n```\n{test['tail']}\n```"))
        diff, stat = diff_of(root)
        last = rec["attempts"][-1]
        status = ("error" if last["stats"]["status"] != "ok" else "no_change" if not diff.strip()
                  else "tests_failed" if test and not test["passed"] else "done")
        out = {"status": status, "worker_id": wid, "base_commit": base_commit, "diff_stat": stat,
               "diff": diff if len(diff) <= DIFF_LIMIT else diff[:DIFF_LIMIT] + "\n... (잘림, 전체는 log 의 diff)",
               "tests": last.get("test"), "attempts": len(rec["attempts"]), "summary": last["final"][-1500:],
               "effort": last["effort"], "efforts_tried": [x["effort"] for x in rec["attempts"]],
               "stats": {"wall_s": round(time.perf_counter() - t_wall), **last["stats"]},
               "worktree": str(root), "log": str(LOGS / f"{wid}.json"),
               "apply_hint": "지휘자 쪽에서 diff 를 검토한 뒤 `git apply` 로 반영한다 (base_commit 기준)."}
        rec.update(result={k: v for k, v in out.items() if k != "diff"}, diff=diff)
        if not keep_worktree:
            out["worktree"] = drop_tree(wid)
        return out
    except Exception as ex:  # noqa: BLE001
        rec["error"] = repr(ex)
        return {"status": "error", "worker_id": wid, "error": str(ex)[:800]}
    finally:
        LOGS.mkdir(parents=True, exist_ok=True)
        (LOGS / f"{wid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        LOCK.unlink(missing_ok=True)


def status() -> dict:
    cfg = load_cfg()
    base, why = find_server(api_key())
    return {"server": base or f"down ({why})", "busy": LOCK.read_text(encoding="utf-8") if LOCK.exists() else None,
            "measuring": measuring(),
            "cfg": cfg, "worktrees": sorted(p.name for p in WORK.iterdir() if p.is_dir() and p.name != "logs") if WORK.exists() else []}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--drop", metavar="WORKER_ID")
    ap.add_argument("--repo")
    ap.add_argument("--ref")
    ap.add_argument("--task")
    ap.add_argument("--task-file")
    ap.add_argument("--files", nargs="*")
    ap.add_argument("--test-cmd")
    ap.add_argument("--max-steps", type=int)
    ap.add_argument("--effort", choices=list(x3.EFFORT_LEVELS), help="노력치 (기본: configs/worker.json 의 effort)")
    ap.add_argument("--no-repair", action="store_true", help="테스트가 실패해도 다시 시도하지 않음")
    ap.add_argument("--diff-only", action="store_true", help="diff 만 표준 출력으로 (나머지는 표준 오류)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.status:
        print(json.dumps(status(), ensure_ascii=False, indent=1))
        return 0
    if a.drop:
        print(drop_tree(a.drop))
        return 0
    task = Path(a.task_file).read_text(encoding="utf-8") if a.task_file else a.task
    if not (a.repo and task):
        ap.error("--repo 와 --task(또는 --task-file)가 필요하다")
    r = delegate(task, a.repo, a.ref, a.files, a.test_cmd, a.max_steps, False if a.no_repair else None, effort=a.effort)
    if a.diff_only:
        print(json.dumps({k: v for k, v in r.items() if k != "diff"}, ensure_ascii=False, indent=1), file=sys.stderr)
        print(r.get("diff", ""), end="")
    else:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0 if r["status"] in ("done", "no_change") else 1


if __name__ == "__main__":
    raise SystemExit(main())
