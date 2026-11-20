"""두 GGUF 의 텐서별 형식을 비교한다(헤더만 읽음). 층 번호를 N 으로 묶어 '이름 꼴 · 형식 A · 형식 B' 별 개수를 출력.
예: M0 와 R0(재현)가 expert 까지 같은지, 후보가 expert 밖에서 M0 와 같은지(G0).
사용: python gguf_types_diff.py A.gguf B.gguf [--experts-only | --no-experts]
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

sys.path.insert(0, r"C:\strata-lab\engine\tools")
from gguf_reader import GGUFFile  # noqa: E402  (STRATA 엔진 저장소의 헤더 파서)


def types(path: str) -> dict[str, str]:
    g = GGUFFile(path)
    return {t.name: (t.type_name if isinstance(getattr(t, "type_name", None), str) else str(t.type)) for t in g.tensors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    m = ap.add_mutually_exclusive_group()
    m.add_argument("--experts-only", action="store_true")
    m.add_argument("--no-experts", action="store_true")
    x = ap.parse_args()
    a, b = types(x.a), types(x.b)
    print(f"tensors {len(a)} vs {len(b)}; only in A {len(set(a) - set(b))}, only in B {len(set(b) - set(a))}")
    diff = collections.Counter()
    for n in sorted(set(a) & set(b)):
        exp = "_exps" in n
        if (x.experts_only and not exp) or (x.no_experts and exp) or a[n] == b[n]:
            continue
        diff[(re.sub(r"blk\.\d+\.", "blk.N.", n), a[n], b[n])] += 1
    if not diff:
        print("same types")
    for (name, ta, tb), c in diff.most_common():
        print(f"{c:4d}  {name}  {ta} -> {tb}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
