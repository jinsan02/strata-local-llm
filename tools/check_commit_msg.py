"""커밋 메시지 검사 — .githooks/commit-msg 의 본체.

규칙 전문은 docs/COMMIT_CONVENTION.md 에 있다. 여기는 그 집행 코드다.

    <type>(<scope>): <제목>

    <본문 — 왜 바꿨는지>

    <트레일러 — 기계가 읽는 계보>

핵심 두 가지
    1. record 커밋은 코드·엔진 패치·설정을 건드릴 수 없다.
       측정 결과를 보고 코드를 슬쩍 고치면서 기록하는 경로를 없앤다 (기획서 5.1).
    2. fix 커밋은 Invalidates 를 반드시 적는다.
       그 버그가 어떤 기존 측정을 무효화하는지 남긴다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import repo  # noqa: E402

TYPES: dict = {
    "record":  "측정·평가 결과 기록 (원장 행 + 산출물). 코드 변경 금지",
    "fix":     "잘못된 동작 수정",
    "upgrade": "기존 기능 개선 (동작은 유지)",
    "feat":    "새 구성요소·스크립트 추가",
    "model":   "모델·양자화 산출물 등록 (M0, M1 ...)",
    "docs":    "문서",
    "chore":   "환경·설정·의존성·훅",
    "revert":  "되돌리기",
}

# 기획서의 단계와 같다: 환경 · 엔진 · 실행 설정 · 양자화 · 측정 · 품질 평가 · 인프라 · 문서
SCOPES: tuple = ("env", "engine", "config", "quant", "bench", "eval", "infra", "docs")

REQUIRED_TRAILERS: dict = {
    "record": ("Run-Id", "Ledger", "Config-SHA256"),
    "fix": ("Invalidates",),
    "model": ("Model-SHA256",),
}

SUBJECT_MAX = 72

# record 커밋에서 스테이지가 허용되는 경로.
RECORD_ALLOWED_PREFIXES = ("experiments/", "reports/", "docs/")

HEADER_RE = re.compile(r"^(?P<type>[a-z]+)\((?P<scope>[a-z]+)\): (?P<subject>.+)$")
TRAILER_RE = re.compile(r"^(?P<key>[A-Z][A-Za-z0-9-]*): (?P<value>.+)$")
RUN_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")


def strip_comments(text: str) -> str:
    lines = [ln for ln in text.replace("\r\n", "\n").split("\n")
             if not ln.startswith("#")]
    for i, ln in enumerate(lines):          # verbose diff 구간 제거
        if ln.startswith("diff --git "):
            lines = lines[:i]
            break
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def parse_trailers(lines: list) -> dict:
    """마지막 연속 블록에서 'Key: value' 트레일러를 읽는다."""
    block: list = []
    for line in reversed(lines):
        if not line.strip():
            break
        block.append(line)
    out: dict = {}
    for line in reversed(block):
        m = TRAILER_RE.match(line.strip())
        if m:
            out[m.group("key")] = m.group("value").strip()
    return out


def _missing_run_hint(source: str) -> str:
    if source != "index":
        return "원장에 없는 run 은 기록할 수 없다"
    return ("원장에 없는 run 은 기록할 수 없다. 작업 트리에는 있는데 이 오류가 나면 "
            "아직 스테이지하지 않은 것이다 — git add experiments/LEDGER.tsv 를 먼저 하라")


def _check_config_sha(run_id: str, claimed, root: Path, source: str) -> list:
    """Config-SHA256 이 원장의 그 run 값과 같은지 본다. 해시를 손으로 적지 않게 한다."""
    if not claimed or not repo.is_sha256(claimed):
        return []
    actual = {r.get("config_sha256") for r in repo.ledger_rows(root, source)
              if r.get("run_id") == run_id} - {"", repo.NA, None}
    if actual and claimed not in actual:
        return [f"Config-SHA256 이 run {run_id!r} 의 원장 값과 다르다.",
                f"    적힌 값: {claimed}",
                f"    원장 값: {sorted(actual)[0]}",
                "    해시를 손으로 적지 마라. 원장에서 읽어와라."]
    return []


def _path_exists(rel: str, root: Path, source: str) -> bool:
    if source == "index":
        return repo.is_staged(rel, root)
    return (root / rel).exists()


def check(message: str, root=None, *, source: str = "worktree", staged=None) -> list:
    """규칙 위반 목록을 돌려준다. 빈 리스트면 통과."""
    root = Path(root or repo.repo_root())
    errors: list = []

    lines = strip_comments(message).split("\n")
    if not lines or not lines[0].strip():
        return ["커밋 메시지가 비어 있다"]
    header = lines[0].rstrip()

    if header.startswith(("Merge ", "Revert ", "fixup!", "squash!")):
        return []

    m = HEADER_RE.match(header)
    if not m:
        return [f"제목 형식이 틀렸다: {header!r}",
                "  올바른 형식: <type>(<scope>): <제목>",
                f"  type  : {', '.join(sorted(TYPES))}",
                f"  scope : {', '.join(SCOPES)}",
                "  예: record(bench): B0 기본 설정 8K 단일 요청 기준선"]

    ctype, scope, subject = m.group("type"), m.group("scope"), m.group("subject")
    if ctype not in TYPES:
        errors.append(f"알 수 없는 type: {ctype!r} (가능: {', '.join(sorted(TYPES))})")
    if scope not in SCOPES:
        errors.append(f"알 수 없는 scope: {scope!r} (가능: {', '.join(SCOPES)})")
    if len(header) > SUBJECT_MAX:
        errors.append(f"제목이 {len(header)}자다. {SUBJECT_MAX}자 이하로 줄여라")
    if subject.endswith("."):
        errors.append("제목 끝에 마침표를 쓰지 않는다")
    if len(lines) > 1 and lines[1].strip():
        errors.append("제목과 본문 사이에 빈 줄이 있어야 한다")

    trailers = parse_trailers(lines[1:]) if len(lines) > 1 else {}
    for key in REQUIRED_TRAILERS.get(ctype, ()):
        if key not in trailers:
            errors.append(f"{ctype} 커밋에는 '{key}:' 트레일러가 필요하다 "
                          "(docs/COMMIT_CONVENTION.md 참조)")

    for key in ("Config-SHA256", "Model-SHA256"):
        value = trailers.get(key)
        if value and not repo.is_sha256(value):
            errors.append(f"{key} 는 소문자 64자리 sha256 이어야 한다: {value!r}")

    known = repo.known_run_ids(root, source)
    run_id = trailers.get("Run-Id")
    if run_id:
        if not RUN_ID_RE.match(run_id):
            errors.append(f"Run-Id 형식이 틀렸다: {run_id!r} (소문자·숫자·_.- 만)")
        elif run_id not in known:
            errors.append(f"Run-Id {run_id!r} 가 {repo.LEDGER} 에 없다. "
                          + _missing_run_hint(source))
        else:
            errors += _check_config_sha(run_id, trailers.get("Config-SHA256"), root, source)

    inv = trailers.get("Invalidates")
    if inv and inv.lower() not in ("none", "없음"):
        for rid in [r.strip() for r in inv.split(",") if r.strip()]:
            if rid not in known:
                errors.append(f"Invalidates 의 run_id {rid!r} 가 원장에 없다. "
                              + _missing_run_hint(source))

    for rel in [p.strip() for p in trailers.get("Ledger", "").split(",") if p.strip()]:
        if not _path_exists(rel, root, source):
            errors.append(f"Ledger 에 적힌 경로가 없다: {rel}")

    if ctype == "record":
        files = repo.staged_files(root) if staged is None else staged
        bad = [f for f in files if not f.startswith(RECORD_ALLOWED_PREFIXES)]
        if bad:
            errors.append("record 커밋은 코드·설정을 건드릴 수 없다. 다음을 분리해서 "
                          "먼저 fix/upgrade/feat/chore 로 커밋하라:")
            errors.extend(f"    {f}" for f in bad[:20])
    return errors


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    source = "index" if "--staged" in args else "worktree"
    args = [a for a in args if a != "--staged"]
    if not args:
        print("usage: check_commit_msg.py [--staged] <COMMIT_MSG_FILE>", file=sys.stderr)
        return 2
    # utf-8-sig: Windows PowerShell 5.1 의 Out-File 이 붙이는 BOM 을 떼어 낸다.
    message = Path(args[0]).read_text(encoding="utf-8-sig", errors="replace")
    # CI(worktree)는 커밋된 트리를 보므로 스테이지 목록이 없다.
    errors = check(message, source=source, staged=None if source == "index" else [])
    if not errors:
        return 0
    print("\n  커밋 거부 — 커밋 메시지 규칙 위반\n", file=sys.stderr)
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    print("\n  규칙: docs/COMMIT_CONVENTION.md\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
