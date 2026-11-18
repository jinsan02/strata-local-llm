"""훅·검사기 공용 — git 인덱스와 원장 읽기 (표준 라이브러리만).

훅은 인덱스(이 커밋이 만들 트리)를, CI 는 커밋된 트리를 본다. 둘이 같은 것을
보도록 원장을 읽는 경로를 한 곳에 둔다 (docs/COMMIT_CONVENTION.md 3번 규칙).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

LEDGER = "experiments/LEDGER.tsv"
NA = "NA"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, timeout=20)
    if out.returncode == 0 and out.stdout.strip():
        return Path(out.stdout.strip())
    return Path(__file__).resolve().parents[1]


def git(*args: str, root: Path) -> str:
    out = subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                         text=True, encoding="utf-8", errors="replace", timeout=30)
    return out.stdout if out.returncode == 0 else ""


def staged_files(root: Path) -> list:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", root=root)
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def is_staged(rel: str, root: Path) -> bool:
    return bool(git("ls-files", "--cached", "--", rel, root=root).strip())


def read_text(rel: str, root: Path, source: str) -> str:
    """source: worktree | index | <commit>"""
    if source == "worktree":
        p = root / rel
        return p.read_text(encoding="utf-8") if p.exists() else ""
    spec = f":{rel}" if source == "index" else f"{source}:{rel}"
    return git("show", spec, root=root)


def ledger_rows(root: Path, source: str = "worktree") -> list:
    text = read_text(LEDGER, root, source).replace("\r\n", "\n")
    lines = [ln for ln in text.split("\n") if ln.strip()]
    if not lines:
        return []
    header = lines[0].split("\t")
    return [dict(zip(header, ln.split("\t"))) for ln in lines[1:]]


def known_run_ids(root: Path, source: str = "worktree") -> set:
    return {r.get("run_id", "") for r in ledger_rows(root, source)} - {""}


def is_sha256(value: str) -> bool:
    return bool(SHA256_RE.match(value or ""))
