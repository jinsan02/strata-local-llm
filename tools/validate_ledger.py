"""원장 무결성 검사 — 스키마는 docs/LEDGER_SCHEMA.md.

    1. 헤더가 스키마와 같다
    2. 모든 행의 열 수가 헤더와 같다
    3. status 는 start | ok | fail
    4. append-only — 직전 커밋(HEAD)의 행이 그대로 앞에 남아 있다
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import repo  # noqa: E402

COLUMNS = (
    "ts_utc", "run_id", "config_id", "phase", "status", "model_id", "model_sha256",
    "engine_commit", "settings_id", "ctx", "parallel", "input_tokens", "output_tokens",
    "pp_tps", "tg_tps", "ttft_ms", "tt_answer_ms", "total_ms", "peak_vram_mb",
    "peak_ram_mb", "git_commit", "git_dirty", "config_sha256", "env_sha256", "note",
)
STATUSES = ("start", "ok", "fail")


def check_text(text: str, head_text: str = "") -> list:
    errors: list = []
    lines = [ln for ln in text.replace("\r\n", "\n").split("\n") if ln != ""]
    if not lines:
        return [f"{repo.LEDGER}: 비어 있다 (헤더가 있어야 한다)"]
    header = tuple(lines[0].split("\t"))
    if header != COLUMNS:
        errors.append(f"{repo.LEDGER}: 헤더가 스키마와 다르다 (docs/LEDGER_SCHEMA.md)")
    for i, ln in enumerate(lines[1:], start=2):
        cells = ln.split("\t")
        if len(cells) != len(header):
            errors.append(f"{repo.LEDGER}:{i}: 열 {len(cells)}개, 헤더는 {len(header)}개")
            continue
        status = cells[header.index("status")] if "status" in header else ""
        if status not in STATUSES:
            errors.append(f"{repo.LEDGER}:{i}: status {status!r} (가능: {', '.join(STATUSES)})")
    old = [ln for ln in head_text.replace("\r\n", "\n").split("\n") if ln != ""]
    if old and old[0] == lines[0] and lines[:len(old)] != old:
        errors.append(f"{repo.LEDGER}: 기존 행이 바뀌었다. 원장은 append-only — 정정도 새 행이다")
    return errors


def validate(root=None, source: str = "worktree") -> list:
    root = Path(root or repo.repo_root())
    text = repo.read_text(repo.LEDGER, root, source)
    head = repo.read_text(repo.LEDGER, root, "HEAD") if source == "index" else ""
    return check_text(text, head)


def main() -> int:
    errors = validate()
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
