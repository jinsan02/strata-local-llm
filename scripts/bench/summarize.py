"""원장 집계 — run_id 의 _r<n> 을 떼어 묶고 중앙값 · 표준편차 · 반복 수를 낸다 (RULES 6).

    python scripts/bench/summarize.py --prefix x1_ --out reports/x1-summary.md
"""

from __future__ import annotations

import argparse
import re
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "experiments" / "LEDGER.tsv"
METRICS = ("input_tokens", "output_tokens", "pp_tps", "tg_tps", "ttft_ms", "tt_answer_ms", "total_ms",
           "peak_vram_mb", "peak_ram_mb", "ssd_read_mb")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def fmt(vals, digits=1):
    vals = [v for v in vals if v is not None]
    if not vals:
        return "NA"
    med = st.median(vals)
    sd = st.stdev(vals) if len(vals) > 1 else 0.0
    return f"{med:,.{digits}f} ± {sd:,.{digits}f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    hdr = lines[0].split("\t")
    groups = defaultdict(list)
    for ln in lines[1:]:
        row = dict(zip(hdr, ln.split("\t")))
        if not row["run_id"].startswith(a.prefix):
            continue
        groups[re.sub(r"_r\d+$", "", row["run_id"])].append(row)
    out = [f"# 집계: `{a.prefix}*` (중앙값 ± 표준편차, n = 반복 수)", "",
           "| run | ctx | 입력 | 출력 | n | fail | PP tok/s | TG tok/s | 첫 스트림 ms | 첫 답변 ms | 완료 ms | Peak VRAM MB | 엔진 RAM MB | SSD MB |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for key in sorted(groups, key=lambda k: (int(groups[k][0]["ctx"]), num(groups[k][0]["input_tokens"]) or 0, k)):
        rows = groups[key]
        ok = [r for r in rows if r["status"] == "ok"]
        col = lambda m: [num(r[m]) for r in ok]  # noqa: E731
        out.append(f"| {key} | {rows[0]['ctx']} | {fmt(col('input_tokens'), 0)} | {fmt(col('output_tokens'), 0)} | {len(ok)} | "
                   f"{len(rows) - len(ok)} | {fmt(col('pp_tps'))} | {fmt(col('tg_tps'))} | {fmt(col('ttft_ms'), 0)} | "
                   f"{fmt(col('tt_answer_ms'), 0)} | {fmt(col('total_ms'), 0)} | {fmt(col('peak_vram_mb'), 0)} | "
                   f"{fmt(col('peak_ram_mb'), 0)} | {fmt(col('ssd_read_mb'), 0)} |")
    text = "\n".join(out) + "\n"
    print(text)
    if a.out:
        p = ROOT / a.out
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
