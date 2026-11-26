"""tools/repo.py 의 error_type_of · is_pass 단위 테스트 (지휘자가 먼저 쓴 것, 11-26 실사용 시연 R2).

'통과' 판정은 이 함수 하나로 한다(COLLAB-LOG C-021: 접두사로 세면 pass_partial_apply 가 섞였다).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import repo  # noqa: E402


def test_error_type_of_reads_marker_from_note():
    note = "edit_file ok 2 fail 0; regress 0; error_type pass; fmt ok; model_ms 1234"
    assert repo.error_type_of(note) == "pass"


def test_error_type_of_keeps_underscored_types_whole():
    assert repo.error_type_of("x; error_type pass_partial_apply; y") == "pass_partial_apply"
    assert repo.error_type_of("error_type import_or_syntax") == "import_or_syntax"


def test_error_type_of_missing_or_empty_is_none():
    assert repo.error_type_of("resolved True; fmt ok") is None
    assert repo.error_type_of("") is None
    assert repo.error_type_of(None) is None


def test_error_type_of_takes_first_marker():
    assert repo.error_type_of("error_type test_fail; later error_type pass") == "test_fail"


def test_error_type_of_accepts_ledger_row():
    assert repo.error_type_of({"run_id": "x3h12_r1", "note": "a; error_type test_fail"}) == "test_fail"
    assert repo.error_type_of({"run_id": "x"}) is None


def test_is_pass_is_exact_match_only():
    assert repo.is_pass("error_type pass") is True
    assert repo.is_pass({"note": "error_type pass; (not passed)"}) is True
    assert repo.is_pass("error_type pass_partial_apply") is False
    assert repo.is_pass("error_type test_fail") is False
    assert repo.is_pass("") is False
    assert repo.is_pass(None) is False
