"""훅 본체 단위 테스트 — GPU·네트워크 없이 돈다 (CI 와 같은 조건)."""

from pathlib import Path

from tools import check_commit_msg as ccm
from tools import precheck, validate_ledger

ROOT = Path(__file__).resolve().parents[1]


def errs(msg, staged=()):
    return ccm.check(msg, ROOT, source="worktree", staged=list(staged))


def test_good_chore():
    assert errs("chore(env): Anaconda 와 conda 환경을 설치한다\n\n왜 필요한지.\n") == []


def test_bad_header():
    assert errs("Prepare desktop for experiments")


def test_unknown_scope_and_period():
    e = errs("docs(readme): 설명.")
    assert any("scope" in x for x in e) and any("마침표" in x for x in e)


def test_subject_length():
    assert errs("docs(docs): " + "가" * 70)


def test_blank_line_required():
    assert errs("docs(docs): 제목\n본문")


def test_fix_requires_invalidates():
    assert errs("fix(bench): 첫 답변 지연 계산 오류")
    assert errs("fix(bench): 첫 답변 지연 계산 오류\n\n이유.\n\nInvalidates: none") == []


def test_record_requires_trailers_and_no_code():
    e = errs("record(bench): B0 기준선\n\n이유.", staged=["tools/x.py"])
    assert any("Run-Id" in x for x in e)
    assert any("record 커밋은 코드" in x for x in e)


def test_model_sha_format():
    assert errs("model(quant): M1 등록\n\n이유.\n\nModel-SHA256: ABC")


def test_precheck_blocks():
    files = ["final_eval/answers.json", "data/x.gguf", "engine/a.cu", "m.gguf", "docs/a.md"]
    e = precheck.check_paths(files, ROOT, size_of=lambda p, r: 0)
    assert len(e) == 4


def test_ledger_header_ok():
    header = "\t".join(validate_ledger.COLUMNS)
    assert validate_ledger.check_text(header + "\n") == []


def test_ledger_append_only():
    header = "\t".join(validate_ledger.COLUMNS)
    n = len(validate_ledger.COLUMNS)
    row = "\t".join(["x"] * 4 + ["ok"] + ["x"] * (n - 5))
    row2 = "\t".join(["y"] * 4 + ["ok"] + ["y"] * (n - 5))
    assert validate_ledger.check_text(f"{header}\n{row2}\n", f"{header}\n{row}\n")
    assert validate_ledger.check_text(f"{header}\n{row}\n{row2}\n", f"{header}\n{row}\n") == []
