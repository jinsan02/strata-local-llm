"""H7 (25-3) 사전 분석: 도구 편집이 없던(작업 복사본이 처음 그대로인) 실행의 마지막 답을 strict 와 lenient 로 다시 적용해 채점한다.
모델 · 서버 없음. python replay_edit_apply.py <run_x3.py 폴더> <set prefix ...>"""
import sys, re, json, csv, pathlib, collections, shutil
sys.path.insert(0, sys.argv[1])
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.repo import error_type_of  # noqa: E402
import run_x3 as x3  # noqa: E402

R = pathlib.Path(r"C:\strata-lab")
RUNS = R / "experiments" / "runs"
rows = {r["run_id"]: r for r in csv.DictReader(open(R / "experiments/LEDGER.tsv", encoding="utf-8"), delimiter="\t")}


def shift(s: str, d: int) -> str | None:
    out = []
    for ln in s.split("\n"):
        if not ln.strip():
            out.append(ln.strip(" \t"))
            continue
        if d < 0:
            if ln[:-d] != " " * (-d):
                return None
            out.append(ln[-d:])
        else:
            out.append(" " * d + ln)
    return "\n".join(out)


def rstrip_lines(s: str) -> str:
    return "\n".join(ln.rstrip() for ln in s.split("\n"))


def lenient_pairs(text: str, s: str, r: str):
    """(이름, search, replace) 후보를 순서대로. 정확히 한 번 맞는 첫 후보를 쓴다."""
    yield "exact", s, r
    # 줄 끝 공백 차이: 파일 쪽도 정규화해서 찾아야 하므로 별도 처리(아래 apply_one)
    for d in sorted(range(-16, 17), key=lambda k: (abs(k), k)):
        if d == 0:
            continue
        s2, r2 = shift(s, d), shift(r, d)
        if s2 is not None and r2 is not None:
            yield f"indent{d:+d}", s2, r2


def apply_one(text: str, s: str, r: str):
    hits = []
    for name, s2, r2 in lenient_pairs(text, s, r):
        if text.count(s2) == 1:
            hits.append((name, s2, r2))
            if name == "exact":
                break
    if hits:
        name, s2, r2 = hits[0]
        others = {h[0] for h in hits[1:]}
        return text.replace(s2, r2, 1), name + (f"(also {sorted(others)})" if others else "")
    # 줄 끝 공백 무시
    tl, sl = text.split("\n"), rstrip_lines(s).split("\n")
    n = len(sl)
    found = [i for i in range(len(tl) - n + 1) if [x.rstrip() for x in tl[i:i + n]] == sl]
    if len(found) == 1:
        i = found[0]
        return "\n".join(tl[:i] + r.split("\n") + tl[i + n:]), "rstrip"
    return None, None


def new_apply(root, answer, candidates, deny=("tests",)):
    answer = answer or ""
    strict = [(m.group(1), m.group(2), m.group(3)) for m in x3.EDIT_RE.finditer(answer)]
    blocks = strict or [((x3.PATH_RE.findall(answer[max(0, m.start() - 300): m.start()]) or [None])[-1], m.group(1), m.group(2))
                        for m in x3.LOOSE_RE.finditer(answer)]
    applied, errs, how = 0, [], []
    for path, s, r in blocks:
        done = False
        for tgt in ([path] if path else list(candidates)):
            p = (root / tgt).resolve()
            if not p.exists() or any(d in pathlib.Path(tgt).parts for d in deny):
                continue
            if not s.strip():
                break
            t = p.read_text(encoding="utf-8")
            nt, name = apply_one(t, s, r)
            if nt is not None:
                p.write_text(nt, encoding="utf-8", newline="\n")
                applied += 1; done = True; how.append(name)
                break
        if not done:
            errs.append(f"{path}: no match")
    if not blocks:
        errs.append("편집 블록 없음")
    return applied, errs, how


def main():
    stats = collections.Counter()
    changed = []
    for pref in sys.argv[2:]:
        for d in sorted(RUNS.glob(pref + "_*_nav_*")):
            task = d.name.split("_nav_")[1]
            tcfg = json.loads((x3.TASKS / task / "task.json").read_text(encoding="utf-8"))
            for ans in sorted(d.glob("answer_r*.md")):
                i = ans.stem.split("_r")[1]
                rid = f"{d.name}_r{i}"
                row = rows.get(rid)
                if not row:
                    continue
                note = row["note"]
                m = re.search(r"edit_file ok (\d+)", note)
                et0 = error_type_of(note)
                if not m or int(m.group(1)) > 0:
                    stats["skip_tool_edits"] += 1
                    continue
                text = ans.read_text(encoding="utf-8")
                turns = json.loads((d / f"turns_r{i}.json").read_text(encoding="utf-8"))
                last = turns[-1]
                if not text.strip():
                    rej = last.get("rejected")
                    stats[f"empty:{'rejected_call' if rej else 'no_content'}"] += 1
                    continue
                tools = json.loads((d / f"tools_r{i}.json").read_text(encoding="utf-8"))
                cands = sorted({t["args"].get("path") for t in tools if t["tool"] == "read_file" and t.get("ok", True)
                                and isinstance(t["args"], dict) and t["args"].get("path")})
                root = x3.fresh_copy(f"replay-{task}")
                a0, e0 = x3.apply_edits(root, text, cands)
                shutil.rmtree(root, ignore_errors=True)
                root = x3.fresh_copy(f"replay-{task}")
                x3.EDIT_APPLY = "lenient"; a1, e1 = x3.apply_edits(root, text, cands); x3.EDIT_APPLY = "strict"; how = x3.LAST_FORMAT["flags"]; e1 = [] if e1 == ["편집 블록 없음"] and a1 else e1
                key = f"{et0}: old {a0}/{a0 + len(e0) - (1 if e0 == ['편집 블록 없음'] else 0)} -> new {a1}/{a1 + len(e1)}"
                stats["text_answers"] += 1
                if a1 > a0:
                    hidden_src = (x3.TASKS / task / "private" / "test_x3_hidden.py").read_text(encoding="utf-8")
                    gr = x3.grade(root, tcfg, 0)
                    changed.append((rid, et0, row.get("tests_passed"), a0, a1, how, gr["hidden"], gr["ok"]))
                    stats["improved_apply"] += 1
                    stats["improved_pass"] += int(gr["ok"])
                elif et0 in ("apply_fail", "pass_partial_apply") or e1:
                    stats["still_fail"] += 1
                    print("STILL", rid, key)
    for k, v in sorted(stats.items()):
        print(k, v)
    for c in changed:
        print("CHANGED", c)


main()
