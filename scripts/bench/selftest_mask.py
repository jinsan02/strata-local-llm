"""L2 관찰 마스킹(--mask on) 자체 점검 (모델 · 서버 없이). python selftest_mask.py <run_x3.py 폴더>"""
import sys, json, tempfile, pathlib, types
sys.path.insert(0, sys.argv[1])
import run_x3 as x3  # noqa: E402

fails = 0


def check(name, cond):
    global fails
    print(("ok  " if cond else "FAIL"), name)
    fails += 0 if cond else 1


# 1) mask_old_outputs: 최근 2개 · 짧은 것 · edit_file 은 남기고 오래된 것부터, 목표에 닿으면 멈춤
big = "x" * 3000
msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
meta = []
for i, (fn, body) in enumerate([("read_file", big), ("grep", "short"), ("edit_file", big), ("read_file", big), ("read_file", big), ("read_file", big), ("read_file", big)]):
    msgs.append({"role": "assistant", "content": "", "tool_calls": [{"id": str(i), "function": {"name": fn, "arguments": "{}"}}]})
    meta.append((len(msgs), fn, {"path": f"f{i}.py", "start_line": 10 * i}))
    msgs.append({"role": "tool", "tool_call_id": str(i), "content": body})
masked = set()
n, freed = x3.mask_old_outputs(msgs, meta, in_now=8000, masked=masked, mask_to=4500, keep=2, min_chars=400, cpt=1.0)
check("오래된 큰 결과만 지움 (read 0 · 3 → 2개면 목표 도달)", n == 2 and meta[0][0] in masked and meta[3][0] in masked)
check("짧은 grep · edit_file · 최근 2개는 그대로", msgs[meta[1][0]]["content"] == "short" and msgs[meta[2][0]]["content"] == big
      and msgs[meta[5][0]]["content"] == big and msgs[meta[6][0]]["content"] == big)
check("자리표시에 경로 · 줄 범위 · 글자 수", "f0.py" in msgs[meta[0][0]]["content"] and "3000자" in msgs[meta[0][0]]["content"])
check("서버로 가는 메시지에 사적인 키 없음", all(set(m) <= {"role", "content", "tool_calls", "tool_call_id"} for m in msgs))
n2, _ = x3.mask_old_outputs(msgs, meta, in_now=99999, masked=masked, mask_to=0, keep=2, min_chars=400, cpt=1.0)
check("다시 부르면 이미 지운 것은 건너뛰고 남은 것만", n2 == 1 and meta[4][0] in masked)

# 2) navigate_loop 통합: 가짜 모델이 큰 파일을 계속 읽음, 가짜 counter = 글자 수 / 3
root = pathlib.Path(tempfile.mkdtemp())
(root / "big.py").write_text("\n".join(f"line_{i} = {i}  # " + "p" * 60 for i in range(3000)), encoding="utf-8")


def counter(m, t):
    return int(sum(len(x.get("content") or "") for x in m) / 3)


state = {"n": 0}


def chat(base, key, m, mt, to, tools):
    state["n"] += 1
    if tools and state["n"] <= 8:
        args = json.dumps({"path": "big.py", "start_line": 1 + 300 * (state["n"] - 1), "end_line": 300 * state["n"]})
        msg = {"content": "", "tool_calls": [{"id": f"c{state['n']}", "type": "function", "function": {"name": "read_file", "arguments": args}}]}
    else:
        msg = {"content": "끝"}
    return {"choices": [{"message": msg, "finish_reason": "stop"}], "usage": {"prompt_tokens": counter(m, tools), "completion_tokens": 5}}, 1.0


def run(mask):
    state["n"] = 0
    a = types.SimpleNamespace(max_steps=20, budget=8192, ctx=32768, timeout=10, base_url="x", force_at=22272, final_turn="none",
                              mask=mask, reasoning_echo="none", tool_out="chars")
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
    return x3.navigate_loop(root, msgs, a, "k", ("tests",), chat=chat, counter=counter), msgs


r_off, _ = run("off")
r_on, m_on = run("on")
check("off: 마스킹 없음 · 강제 턴에 닿음", r_off["masks"] == 0 and r_off["forced_turns"] >= 1)
check("on: 마스킹이 일어나고 강제 턴 없이 8번 다 읽음", r_on["masks"] >= 1 and r_on["forced_turns"] == 0 and len(r_on["tool_log"]) == 8)
check("on: 마스킹 뒤 입력이 MASK_TO 근처로 내려감", all(e["in_after"] <= x3.MASK_TO + 4100 and e["in_after"] < e["in_before"] for e in r_on["mask_log"]))
check("on: 마지막 2개 도구 결과는 원문", all("문맥 절약" not in m["content"] for m in [x for x in m_on if x["role"] == "tool"][-2:]))
check("on: 턴마다 지우지 않음 (마스킹 수 < 도구 호출 수)", r_on["masks"] < len(r_on["tool_log"]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
