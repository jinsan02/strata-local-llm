"""MTP 초안이 언제 시도되는지 확인한다 (STATE Q10). 같은 프롬프트를 샘플링 조건만 바꿔 보낸다.

    python scripts/bench/mtp_probe.py

서버 /metrics 의 요청별 drafts_offered / drafts_accepted 와 엔진 로그의 "drafts accepted N of M" 을 본다.
"""

from __future__ import annotations

import json
import urllib.request

BASE = "http://127.0.0.1:8080"
PROMPT = "파이썬으로 리스트에서 중복을 제거하면서 순서를 유지하는 함수를 작성하고 짧게 설명하라."
CASES = {
    "a_greedy": {"temperature": 0.0},
    "b_t1_nopenalty": {"temperature": 1.0, "top_p": 0.95, "top_k": 20, "seed": 42},
    "c_t1_presence1.5": {"temperature": 1.0, "top_p": 0.95, "top_k": 20, "presence_penalty": 1.5, "seed": 42},
    "d_server_default": {},
}


def post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def last_request():
    with urllib.request.urlopen(BASE + "/metrics", timeout=15) as r:
        return (json.loads(r.read()).get("requests") or [{}])[-1]


for name, samp in CASES.items():
    res = post("/v1/chat/completions", {"model": "strata", "max_tokens": 256,
                                         "messages": [{"role": "user", "content": PROMPT}], **samp})
    m, t = last_request(), res.get("timings") or {}
    print(json.dumps({"case": name, "sampling": samp, "drafts_offered": m.get("drafts_offered"),
                      "drafts_accepted": m.get("drafts_accepted"), "timings_draft_n": t.get("draft_n"),
                      "timings_draft_accepted": t.get("draft_n_accepted"), "tg_tps": t.get("predicted_per_second"),
                      "finish": res["choices"][0].get("finish_reason")}, ensure_ascii=False))
