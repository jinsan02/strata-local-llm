"""--sampling (S1) 자체 점검 — 서버 불필요.

    python selftest_sampling.py <run_x3.py 가 있는 폴더>
확인: (1) 기본 세트가 지금 값과 같고 config 직렬화가 바뀌지 않는다, (2) card-coding 이 요청 본문에 그대로 들어간다,
(3) 다시 card-general 로 돌리면 원래와 같다, (4) 채점 환경 freeze 해시가 64자 16진수다,
(5) --seed-per-rep 이 회차마다 seed 42+i-1 을 넣고 config 에 seed_policy 를 남긴다.
"""
from __future__ import annotations

import io
import json
import re
import sys

sys.path.insert(0, sys.argv[1])
import run_bench as rb  # noqa: E402

ORIG = dict(rb.SAMPLING)
ORIG_CANON = rb.canon({"sampling": rb.SAMPLING})
import run_x3 as x3  # noqa: E402

fails = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (f"  {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


sent = []


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_urlopen(req, timeout=None):
    sent.append(json.loads(req.data.decode("utf-8")))
    return FakeResp(json.dumps({"choices": [{"message": {"content": "x"}}], "usage": {}}).encode())


x3.urllib.request.urlopen = fake_urlopen

check("기본 세트 = 지금 값", x3.SAMPLING_SETS["card-general"] == ORIG, str(ORIG))
x3.apply_sampling("card-general")
check("card-general 적용 뒤 config 직렬화 불변", rb.canon({"sampling": rb.SAMPLING}) == ORIG_CANON)
x3.apply_sampling("card-coding")
x3.chat_once("http://127.0.0.1:1", "k", [{"role": "user", "content": "hi"}], 16, 5)
body = sent[-1]
check("card-coding: temperature 0.6", body.get("temperature") == 0.6, str(body))
check("card-coding: presence_penalty 0", body.get("presence_penalty") == 0.0, str(body))
check("card-coding: top_p · top_k · seed", (body.get("top_p"), body.get("top_k"), body.get("seed")) == (0.95, 20, 42), str(body))
check("같은 dict (rb.SAMPLING 을 고침)", x3.rb.SAMPLING is rb.SAMPLING)
x3.apply_sampling("card-general")
x3.chat_once("http://127.0.0.1:1", "k", [{"role": "user", "content": "hi"}], 16, 5)
check("card-general 로 되돌림", {k: sent[-1].get(k) for k in ORIG} == ORIG, str(sent[-1]))
# --seed-per-rep (11-19 저녁)
from pathlib import Path  # noqa: E402
src = Path(x3.__file__).read_text(encoding="utf-8")
check("--seed-per-rep 인자", '"--seed-per-rep", action="store_true"' in src)
check("회차 seed 대입이 반복문 바로 안", 'range(a.rep_start, a.rep_start + a.repeat):\n                if a.seed_per_rep:\n                    rb.SAMPLING["seed"] = SEED_BASE + i - 1\n' in src)
check("config 에 seed_policy (navigate · preload)", src.count('**({"seed_policy": SEED_POLICY} if a.seed_per_rep else {})') == 2)
check("SEED_BASE 42", x3.SEED_BASE == 42)
x3.apply_sampling("card-coding")
rb.SAMPLING["seed"] = x3.SEED_BASE + 3 - 1
x3.chat_once("http://127.0.0.1:1", "k", [{"role": "user", "content": "hi"}], 16, 5)
check("회차 3 → 요청 seed 44 · 세트 유지", (sent[-1].get("seed"), sent[-1].get("temperature")) == (44, 0.6), str(sent[-1]))
x3.apply_sampling("card-general")
check("세트 다시 적용하면 seed 42", rb.SAMPLING == ORIG, str(rb.SAMPLING))
h = x3.freeze_sha(x3.PYX)
check("채점 환경 freeze 해시", bool(re.fullmatch(r"[0-9a-f]{64}", h)), h)
print("FAIL 없음 — 전부 통과" if not fails else f"FAIL {len(fails)}: {fails}")
sys.exit(1 if fails else 0)
