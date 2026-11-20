"""bartowski calibration-v6 원본을 Qwen3.6 채팅 템플릿으로 렌더링하고, 우리 보정 세트와 섞어 imatrix 용 파일을 만든다
(11-20 사용자: 공개 보정 세트로 imatrix 비교 추가, 'V6 혼합').

입력: data/calib/bartowski-v6/v6_conversations.json(대화 137개, hermes_reasoning_tool_use, Apache-2.0) · v6_prose.txt(글 54개),
      팩의 tokenizer/chat_template.jinja(M0 와 같은 템플릿), 우리 보정 세트(scripts/quant/build_calib.py 의 calib.txt).
렌더링: 원본 안내대로 add_generation_prompt=False, tools=대화의 tools. tojson 은 HF transformers 처럼 json.dumps(ensure_ascii=False)
(jinja2 기본 tojson 은 <, >, & 를 \\u003c 등으로 바꿔 모델이 실제로 보는 글과 달라진다).
섞기: 세 출처(V6 대화 · V6 글 · 우리 세트)를 조각 단위로 번갈아 놓는다 - llama-imatrix 는 앞에서부터 청크를 쓰므로
--chunks 로 잘라도 세 출처가 고르게 들어간다. llama-imatrix 는 --parse-special 로 돌린다.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import jinja2


def tojson(x, indent=None):
    return json.dumps(x, ensure_ascii=False, indent=indent)


def raise_exception(msg):
    raise jinja2.TemplateError(msg)


def chunks(text: str, size: int) -> list[str]:
    """빈 줄 경계에서 약 size 글자씩 자른다."""
    out, cur = [], []
    n = 0
    for para in text.split("\n\n"):
        cur.append(para)
        n += len(para) + 2
        if n >= size:
            out.append("\n\n".join(cur) + "\n\n")
            cur, n = [], 0
    if cur:
        out.append("\n\n".join(cur) + "\n\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--v6", default=r"C:\strata-lab\data\calib\bartowski-v6")
    ap.add_argument("--template", default=r"C:\strata-lab\data\packs\qwen36-ud-q4_k_xl\tokenizer\chat_template.jinja")
    ap.add_argument("--ours", required=True, help="build_calib.py 의 calib.txt")
    ap.add_argument("--out-v6", required=True, help="V6 만 렌더링한 파일")
    ap.add_argument("--out-mix", required=True, help="V6 + 우리 세트를 번갈아 섞은 파일")
    ap.add_argument("--extension", action="store_true", help="extension_conversations 36개도 넣는다(기본: 기본 137개만)")
    a = ap.parse_args()
    v6 = pathlib.Path(a.v6)
    data = json.loads((v6 / "v6_conversations.json").read_text(encoding="utf-8"))
    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True, extensions=["jinja2.ext.loopcontrols"])
    env.filters["tojson"] = tojson
    env.globals["raise_exception"] = raise_exception
    tpl = env.from_string(pathlib.Path(a.template).read_text(encoding="utf-8"))
    convs = data["conversations"] + (data["extension_conversations"] if a.extension else [])
    rendered, bad = [], 0
    for c in convs:
        try:
            rendered.append(tpl.render(messages=c["messages"], tools=c.get("tools") or None, add_generation_prompt=False))
        except jinja2.TemplateError as e:
            bad += 1
            print(f"skip conversation {c.get('kept_index')}: {e}", file=sys.stderr)
    prose = chunks((v6 / "v6_prose.txt").read_text(encoding="utf-8"), 2500)
    ours = chunks(pathlib.Path(a.ours).read_text(encoding="utf-8"), 2500)
    pathlib.Path(a.out_v6).write_text("".join(r + "\n" for r in rendered) + "".join(prose), encoding="utf-8")
    n_prose, n_ours = len(prose), len(ours)
    srcs = [[r + "\n" for r in rendered], prose, ours]
    mix, i = [], 0
    while any(srcs):
        s = srcs[i % 3]
        if s:
            mix.append(s.pop(0))
        i += 1
    pathlib.Path(a.out_mix).write_text("".join(mix), encoding="utf-8")
    size = lambda p: pathlib.Path(p).stat().st_size
    print(f"v6 conversations {len(rendered)} rendered ({bad} skipped), prose chunks {n_prose}, ours chunks {n_ours}; "
          f"v6 {size(a.out_v6)} B, mix {size(a.out_mix)} B")
    return 0


if __name__ == "__main__":
    sys.exit(main())
