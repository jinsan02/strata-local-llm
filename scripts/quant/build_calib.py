"""Q1 보정(imatrix) 세트와 G2 KL 세트를 로컬 파일만으로 만든다 (docs/q1-plan-20261120.md 5절, 11-20 사용자 결정 1).

출처: conda 환경의 Python 표준 라이브러리 + 일부 site-packages 소스, 저장소의 한국어 규칙 문서 몇 개.
제외: X3 · SWE 과제 저장소(packaging · flask · pytest · werkzeug)와 그 의존 · 벤더 사본(pluggy · _pytest · pip · setuptools),
테스트 폴더, final_eval/, 실험 로그(experiments/ · engine/ · reports/). 다운로드 없음.
파일마다 경로 sha1 로 보정 / KL / 미사용을 나눈다(결정적, 겹치지 않음). 쓴 파일 목록은 manifest 로 남겨 F1 출처에서 뺀다.

출력: --calib (imatrix 용, 채팅 형식 일부 포함 → llama-imatrix --parse-special), --kl (llama-perplexity KL 용), --manifest (JSON).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

ENV = pathlib.Path(r"C:\ProgramData\anaconda3\envs\strata_local_llm\Lib")
SITE_OK = ["requests", "urllib3", "rich", "textual", "jinja2", "markupsafe", "markdown_it", "mdit_py_plugins", "pygments",
           "yaml", "tomli", "tqdm", "psutil", "idna", "charset_normalizer", "platformdirs", "colorama", "regex", "numpy", "PIL"]
BANNED_SEGS = {"packaging", "flask", "pytest", "_pytest", "werkzeug", "pluggy", "pip", "setuptools", "_distutils_hack",
               "test", "tests", "testing", "idlelib", "lib2to3", "turtledemo", "final_eval", "encodings"}
BANNED_WORDS = ("packaging", "flask", "pytest", "werkzeug", "pluggy")   # 파일 이름에 들어 있어도 뺀다
KO_DOCS = {"calib": ["docs/RULES.md", "docs/WORKFLOW.md", "docs/COMMIT_CONVENTION.md", "docs/ENVIRONMENT.md"],
           "kl": ["STRUCTURE.md", "CONTRIBUTING.md"]}
KO_DROP = ("packaging", "flask", "pytest", "x3", "X3", "swe", "SWE", "final_eval")
GROUP_CAP = {"calib": 12, "kl": 4}   # 패키지(또는 표준 라이브러리 하위 폴더)마다 최대 파일 수
MAX_FILE = 8_000          # 한 파일에서 쓰는 최대 글자 수(파일 수를 늘려 다양성 확보)
REQS = ["이 파일이 무엇을 하는지 읽고 핵심 함수를 설명해줘.", "Read this module and find where errors are handled.",
        "이 코드에서 버그가 생길 만한 곳을 찾아줘.", "Summarize the public API defined in this file.",
        "이 모듈의 테스트를 추가하려면 어디부터 봐야 할지 알려줘."]
THINK = ["파일 내용을 먼저 확인해야 한다.", "I should read the file before answering.", "먼저 해당 모듈을 열어 구조를 본다."]


def bucket(rel: str) -> str:
    h = int(hashlib.sha1(rel.encode("utf-8")).hexdigest(), 16) % 10
    return "calib" if h < 7 else ("kl" if h == 7 else "unused")


def sources():
    files = [p for p in ENV.glob("*.py")] + [p for d in ENV.iterdir() if d.is_dir() and d.name not in ("site-packages",)
                                             for p in d.rglob("*.py")]
    for name in SITE_OK:
        files += list((ENV / "site-packages" / name).rglob("*.py"))
    out = []
    for p in sorted(set(files)):
        rel = str(p.relative_to(ENV))
        segs = rel.lower().replace("/", "\\").split("\\")
        if any(s in BANNED_SEGS for s in segs) or any(w in rel.lower() for w in BANNED_WORDS):
            continue
        out.append((rel, p))
    # 알파벳 순이면 앞쪽 모듈만 쓰이므로 경로 해시 순으로 섞는다(결정적)
    return sorted(out, key=lambda x: hashlib.sha1(("order:" + x[0]).encode("utf-8")).hexdigest())


def chat(rel: str, text: str, i: int) -> str:
    path = rel.replace("\\", "/")
    return (f"<|im_start|>user\n{REQS[i % len(REQS)]} `{path}`<|im_end|>\n<|im_start|>assistant\n<think>\n{THINK[i % len(THINK)]}\n"
            f"</think>\n\n<tool_call>\n<function=read_file>\n<parameter=path>\n{path}\n</parameter>\n</function>\n</tool_call>"
            f"<|im_end|>\n<|im_start|>user\n<tool_response>\n{text}\n</tool_response><|im_end|>\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--calib", required=True)
    ap.add_argument("--kl", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--repo", default=r"C:\strata-lab")
    ap.add_argument("--calib-chars", type=int, default=900_000)
    ap.add_argument("--kl-chars", type=int, default=220_000)
    a = ap.parse_args()
    cap = {"calib": a.calib_chars, "kl": a.kl_chars}
    parts = {"calib": [], "kl": []}
    size = {"calib": 0, "kl": 0}
    man = {"policy": __doc__.strip().splitlines()[0], "env": str(ENV), "files": []}
    n = 0
    per_group: dict[tuple[str, str], int] = {}
    for rel, p in sources():
        b = bucket(rel)
        if b == "unused" or size[b] >= cap[b]:
            continue
        s = rel.split("\\")
        group = s[1] if s[0] == "site-packages" else (s[0] if len(s) > 1 else "stdlib")
        if per_group.get((b, group), 0) >= GROUP_CAP[b]:     # 한 패키지(예: pygments lexers)로 쏠리지 않게
            continue
        try:
            text = p.read_text(encoding="utf-8")[:MAX_FILE]
        except (UnicodeDecodeError, OSError):
            continue
        if len(text) < 400:
            continue
        # 보정 세트는 셋 중 하나를 도구 호출 대화 형식으로(하네스와 같은 꼴), KL 세트는 코드 그대로
        piece = chat(rel, text, n) if (b == "calib" and n % 3 == 0) else f"# file: {rel.replace(chr(92), '/')}\n{text}\n"
        parts[b].append(piece)
        size[b] += len(piece)
        per_group[(b, group)] = per_group.get((b, group), 0) + 1
        man["files"].append({"path": rel, "split": b, "chars": len(text), "chat": b == "calib" and n % 3 == 0,
                             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
        n += 1
    for b, docs in KO_DOCS.items():
        for d in docs:
            f = pathlib.Path(a.repo) / d
            if not f.exists():
                continue
            lines = [ln for ln in f.read_text(encoding="utf-8").splitlines() if not any(w in ln for w in KO_DROP)]
            text = "\n".join(lines)
            parts[b].append(text + "\n")
            size[b] += len(text)
            man["files"].append({"path": d, "split": b, "chars": len(text), "chat": False, "korean_doc": True,
                                 "sha256": hashlib.sha256(f.read_bytes()).hexdigest()})
    for b, out in (("calib", a.calib), ("kl", a.kl)):
        pathlib.Path(out).write_text("".join(parts[b]), encoding="utf-8")
    man["chars"] = size
    man["counts"] = {b: sum(1 for x in man["files"] if x["split"] == b) for b in ("calib", "kl")}
    pathlib.Path(a.manifest).write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"calib {size['calib']} chars / {man['counts']['calib']} files, kl {size['kl']} chars / {man['counts']['kl']} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
