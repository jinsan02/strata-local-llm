"""원장 스키마 이행 — 헤더를 tools/validate_ledger.COLUMNS 로 바꾸고 기존 값은 열 이름으로 옮긴다.

새 열은 NA 로 채운다. 기존 값을 추론해서 채우지 않는다 (예: drafts 0/0 은 '초안 시도 미기록' 이므로 NA).
값을 바꾸거나 행을 지우지 않는다 — 열 위치만 바뀐다. 이행은 chore(infra) 커밋 하나로 한다.

    python tools/migrate_ledger.py            # 미리 보기
    python tools/migrate_ledger.py --write
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.validate_ledger import COLUMNS  # noqa: E402

LEDGER = Path(__file__).resolve().parents[1] / "experiments" / "LEDGER.tsv"


def main() -> int:
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    old = lines[0].split("\t")
    dropped = [c for c in old if c not in COLUMNS]
    if dropped:
        print(f"이행 거부: 새 스키마에 없는 열 {dropped} — 값을 버리게 된다")
        return 1
    out = ["\t".join(COLUMNS)]
    for ln in lines[1:]:
        row = dict(zip(old, ln.split("\t")))
        out.append("\t".join(row.get(c, "NA") for c in COLUMNS))
    added = [c for c in COLUMNS if c not in old]
    print(f"행 {len(lines) - 1}개, 더한 열 {added}")
    if "--write" in sys.argv:
        LEDGER.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
        print("썼다")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
