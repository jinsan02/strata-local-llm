"""워커 위임 기록 route.jsonl을 집계하는 스크립트."""
import argparse
import json
from pathlib import Path


def load(path, since=None):
    """JSONL 파일을 읽어서 유효 행 목록과 bad 라인 수를 반환한다."""
    rows = []
    bad = 0
    p = Path(path)
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                bad += 1
                continue
            if obj.get("fake"):
                continue
            if since is not None:
                ts = obj.get("ts")
                if ts is None:
                    continue
                if ts < since:
                    continue
            rows.append(obj)
    return rows, bad


def summarize(rows):
    """행 목록을 집계해 요약 딕셔너리를 반환한다."""
    by_status = {}
    for r in rows:
        st = r.get("status", "unknown")
        by_status[st] = by_status.get(st, 0) + 1
    by_status = dict(sorted(by_status.items()))
    total = len(rows)
    rejected = by_status.get("rejected", 0)
    delegated = total - rejected
    done = by_status.get("done", 0)
    done_rate = done / delegated if delegated else None
    handoff = delegated - done
    forced = sum(1 for r in rows if r.get("force"))
    return {
        "total": total,
        "by_status": by_status,
        "rejected": rejected,
        "delegated": delegated,
        "done": done,
        "done_rate": done_rate,
        "handoff": handoff,
        "forced": forced,
    }


def main(argv=None):
    """CLI 진입점: argparse로 파싱하고 결과를 JSON으로 출력한다."""
    log_path = Path(__file__).resolve().parents[2] / "work" / "worker" / "logs" / "route.jsonl"
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default=str(log_path))
    parser.add_argument("--since", default=None)
    args = parser.parse_args(argv)
    rows, bad = load(args.log, since=args.since)
    result = summarize(rows)
    result["since"] = args.since
    result["bad_lines"] = bad
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
