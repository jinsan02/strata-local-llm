"""pre-commit 검사 본체 — 저장소에 들어가면 안 되는 것을 막는다.

막는 것
    1. 5MB 초과 파일
    2. 모델·팩 바이너리 확장자 (.gguf 등)
    3. engine/, data/, downloads/ 아래 전부
    4. 경로에 final_eval 이 들어간 모든 파일  ← 기획서 8.1, 최종 평가 50문항 분리
    5. 출력 셀이 남아 있는 .ipynb
    6. 원장 TSV 무결성 위반 (tools/validate_ledger.py)

4번은 이 실험에서 가장 되돌릴 수 없는 실수를 막는 장치다. 최종 평가 정답을 한 번
작업 경로에서 보면 그 다음의 모든 후보 선택이 오염된다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import repo  # noqa: E402
from tools.validate_ledger import validate  # noqa: E402

MAX_BYTES = 5 * 1024 * 1024
BLOCKED_SUFFIXES = (".gguf", ".bin", ".safetensors", ".pack", ".pt", ".npz")
BLOCKED_PREFIXES = ("engine/", "data/", "downloads/")
LOCKBOX_TOKEN = "final_eval"


def staged_size(path: str, root: Path) -> int:
    raw = repo.git("cat-file", "-s", f":{path}", root=root).strip()
    return int(raw) if raw.isdigit() else 0


def check_paths(files: list, root: Path, size_of=staged_size) -> list:
    errors: list = []
    for path in files:
        low = path.lower()
        if LOCKBOX_TOKEN in low:
            errors.append(f"{path}: 최종 평가 세트는 커밋할 수 없다 (docs/RULES.md 2번)")
            continue
        if low.startswith(BLOCKED_PREFIXES):
            errors.append(f"{path}: 커밋 금지 경로다 (.gitignore 확인)")
            continue
        if low.endswith(BLOCKED_SUFFIXES):
            errors.append(f"{path}: 모델·팩 바이너리는 커밋하지 않는다. "
                          "sha256 만 원장에 기록하라")
            continue
        size = size_of(path, root)
        if size > MAX_BYTES:
            errors.append(f"{path}: {size / 1024 / 1024:.1f}MB 로 상한 5MB 를 넘는다")
        if low.endswith(".ipynb"):
            try:
                nb = json.loads(repo.read_text(path, root, "index") or "{}")
            except json.JSONDecodeError:
                nb = {}
            if any(c.get("outputs") or c.get("execution_count") for c in nb.get("cells", [])):
                errors.append(f"{path}: 출력 셀을 비우고 커밋하라")
    return errors


def check(root=None) -> list:
    root = Path(root or repo.repo_root())
    return check_paths(repo.staged_files(root), root) + validate(root, source="index")


def main() -> int:
    errors = check()
    if not errors:
        return 0
    print("\n  커밋 거부 — pre-commit 검사 실패\n", file=sys.stderr)
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    print("\n  규칙: docs/RULES.md   |   --no-verify 로 우회하지 마라\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
