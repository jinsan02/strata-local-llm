"""티켓 여러 개를 차례로 워커(delegate)에 맡기고 결과를 한 폴더에 모은다.

지휘자는 시작 요청 1번 + 끝난 뒤 묶음 검토 1~2번만 쓰려는 용도다(docs/read-batch-measure-20261126.md).

    python scripts/worker/batch.py TICKETS.json            # 이 자리에서 돈다
    python scripts/worker/batch.py TICKETS.json --detach   # WMI 로 분리 실행(ssh 를 끊어도 산다, T-012) 후 바로 끝남

TICKETS.json = [{"id": "q1", "task": "...", "files": [...], "test_cmd": "...", "effort": "high"}, ...]
  repo 기본 이 저장소 루트, ref 기본 HEAD. 티켓에 repo · ref 를 따로 줄 수 있다.
결과: work/worker/batch/<배치 id>/
  <n>-<id>.json   delegate 결과(diff 뺀 것)        <n>-<id>.diff   전체 diff(로그 기준, 잘리지 않음)
  batch.log       진행 기록                         summary.md      티켓별 상태 · 시간 · 로컬 토큰 표
  DONE            끝나면 생기는 표시(내용 = 요약 한 줄)
작업 트리는 diff 를 저장한 뒤 지운다. 반영(git apply)은 지휘자가 검토한 뒤 직접 한다.
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
OUT_BASE = ROOT / "work" / "worker" / "batch"


def detach(tickets: Path, bid: str) -> int:
    """Win32_Process.Create 로 자신을 다시 띄운다. ssh 세션의 자식이 아니므로 세션이 끝나도 산다."""
    cmd = f'"{sys.executable}" -I "{Path(__file__).resolve()}" "{tickets.resolve()}" --id {bid}'
    ps = ("$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments "
          f"@{{CommandLine = '{cmd}'; CurrentDirectory = '{ROOT}'}}; "
          "Write-Output (\"{0} {1}\" -f $r.ReturnValue, $r.ProcessId)")
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    rc, _, pid = (r.stdout.strip() + "  ").partition(" ")
    print(json.dumps({"batch_id": bid, "out": str(OUT_BASE / bid), "wmi_rc": rc, "pid": pid.strip(),
                      "stderr": r.stderr.strip()[-300:]}, ensure_ascii=False))
    return 0 if rc == "0" else 1


def run(tickets: list, bid: str) -> int:
    import strata_worker as sw  # 분리 실행에서도 같은 워커 코드를 쓴다
    out = OUT_BASE / bid
    out.mkdir(parents=True, exist_ok=True)
    log = (out / "batch.log").open("a", encoding="utf-8")

    def say(msg):
        log.write(f"{datetime.now():%H:%M:%S} {msg}\n")
        log.flush()

    say(f"start {len(tickets)} tickets")
    rows, t0 = [], time.time()
    for n, t in enumerate(tickets, 1):
        tid = t.get("id") or f"t{n}"
        stem = f"{n:02d}-{tid}"
        say(f"[{stem}] delegate")
        ts = time.time()
        try:
            r = sw.delegate(t["task"], t.get("repo", str(ROOT)), t.get("ref"), t.get("files"), t.get("test_cmd"),
                            effort=t.get("effort"), keep_worktree=True)
        except Exception as ex:  # noqa: BLE001 - 한 티켓이 실패해도 다음 티켓으로
            r = {"status": "error", "error": repr(ex)[:800]}
        wall = round(time.time() - ts)
        diff = r.get("diff", "")
        wid = r.get("worker_id")
        if wid:
            lp = sw.LOGS / f"{wid}.json"
            if lp.exists():
                diff = json.loads(lp.read_text(encoding="utf-8")).get("diff", diff)
            r["worktree"] = sw.drop_tree(wid)
        # newline="" : Windows 에서 \n 을 CRLF 로 바꾸면 LF 원본에 git apply 가 안 된다(T-031)
        with open(out / f"{stem}.diff", "w", encoding="utf-8", newline="") as fh:
            fh.write(diff or "")
        (out / f"{stem}.json").write_text(json.dumps({k: v for k, v in r.items() if k != "diff"}, ensure_ascii=False,
                                                     indent=1, default=str), encoding="utf-8")
        st = r.get("stats") or {}
        tests = r.get("tests") or {}
        rows.append({"n": n, "id": tid, "status": r["status"], "wall_s": wall, "attempts": r.get("attempts"),
                     "model_calls": st.get("model_calls"), "out_tok": st.get("out_tok"), "max_in": st.get("max_in"),
                     "tests": tests.get("passed"), "diff_stat": (r.get("diff_stat") or "").strip().splitlines()[-1:],
                     "worker_id": wid})
        say(f"[{stem}] {r['status']} {wall}s")
    total = round(time.time() - t0)
    ok = sum(x["status"] == "done" for x in rows)
    lines = [f"# 배치 {bid}", "", f"티켓 {len(rows)} · done {ok} · 전체 {total}초", "",
             "| # | id | 상태 | 초 | 시도 | 모델 호출 | 출력 토큰 | 최대 입력 | 테스트 | diff |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for x in rows:
        lines.append(f"| {x['n']} | {x['id']} | {x['status']} | {x['wall_s']} | {x['attempts']} | {x['model_calls']} | "
                     f"{x['out_tok']} | {x['max_in']} | {x['tests']} | {' '.join(x['diff_stat'])} |")
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    say(f"done {ok}/{len(rows)} {total}s")
    (out / "DONE").write_text(f"done {ok}/{len(rows)} {total}s\n", encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tickets")
    ap.add_argument("--detach", action="store_true", help="WMI 로 분리 실행하고 바로 끝난다")
    ap.add_argument("--id", help="배치 id (기본: 시각)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    bid = a.id or datetime.now().strftime("%Y%m%d-%H%M%S")
    tickets = json.loads(Path(a.tickets).read_text(encoding="utf-8"))
    if a.detach:
        return detach(Path(a.tickets), bid)
    return run(tickets, bid)


if __name__ == "__main__":
    raise SystemExit(main())
