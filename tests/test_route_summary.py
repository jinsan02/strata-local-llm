"""scripts/worker/route_summary.py 단위 테스트 (지휘자가 먼저 쓴 것, 11-26 실사용 시연 R1)."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("route_summary", ROOT / "scripts" / "worker" / "route_summary.py")
rs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rs)


def _write(tmp_path, lines):
    p = tmp_path / "route.jsonl"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def _row(ts, status, **kw):
    r = {"ts": ts, "status": status, "worker_id": "w", "repo": "C:\r", "files": 1,
         "test_cmd": True, "blocks": [], "warnings": [], "force": False}
    r.update(kw)
    return json.dumps(r, ensure_ascii=False)


def test_load_skips_fake_blank_and_bad_lines(tmp_path):
    p = _write(tmp_path, [
        _row("2026-11-26 10:40:00", "done"),
        "",
        "{not json",
        _row("2026-11-26 10:41:00", "done", fake=True),
    ])
    rows, bad = rs.load(p)
    assert [r["status"] for r in rows] == ["done"]
    assert bad == 1


def test_load_since_is_inclusive_and_drops_rows_without_ts(tmp_path):
    no_ts = json.dumps({"status": "done"})
    p = _write(tmp_path, [
        _row("2026-11-25 09:00:56", "done"),
        _row("2026-11-26 10:30:00", "tests_failed"),
        _row("2026-11-26 11:00:00", "done"),
        no_ts,
    ])
    rows, bad = rs.load(p, since="2026-11-26 10:30:00")
    assert [r["status"] for r in rows] == ["tests_failed", "done"]
    assert bad == 0
    rows_all, _ = rs.load(p)
    assert len(rows_all) == 4


def test_summarize_counts_and_rates():
    rows = [
        {"status": "done"}, {"status": "done"}, {"status": "tests_failed"},
        {"status": "rejected"}, {"status": "no_change", "force": True}, {"status": "error"},
    ]
    s = rs.summarize(rows)
    assert s["total"] == 6
    assert s["by_status"] == {"done": 2, "error": 1, "no_change": 1, "rejected": 1, "tests_failed": 1}
    assert s["rejected"] == 1
    assert s["delegated"] == 5          # rejected 를 뺀 실제 실행
    assert s["done"] == 2
    assert s["done_rate"] == 0.4        # done / delegated
    assert s["handoff"] == 3            # 실행됐지만 done 이 아님
    assert s["forced"] == 1


def test_summarize_empty_has_none_rates():
    s = rs.summarize([])
    assert s["total"] == 0 and s["delegated"] == 0 and s["done"] == 0
    assert s["done_rate"] is None
    assert s["by_status"] == {}


def test_main_prints_json(tmp_path, capsys):
    p = _write(tmp_path, [_row("2026-11-26 10:40:00", "done"), _row("2026-11-26 10:50:00", "rejected")])
    rc = rs.main(["--log", str(p), "--since", "2026-11-26 10:30:00"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["total"] == 2 and out["done"] == 1 and out["done_rate"] == 1.0
    assert out["since"] == "2026-11-26 10:30:00" and out["bad_lines"] == 0
