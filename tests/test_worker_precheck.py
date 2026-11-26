"""워커 위임 전 확인(precheck) · 지휘자 넘기기(handoff) 단위 테스트 (11-26 실사용 시연 R4).

selftest_worker.py 8 · 9 번은 가짜 모델까지 돌리는 통합 점검이라 CI 에 없다. 여기서는 판단 규칙만
서버 · 모델 없이 본다(git 만 필요). 기준: docs/delegation-20261124.md 2절.
"""
import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("strata_worker", ROOT / "scripts" / "worker" / "strata_worker.py")
w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(w)

CFG = {"ctx": 65536}
TASK = "calc.py 의 sub(a, b) 가 a + b 를 돌려준다. a - b 를 돌려주게 고친다. 다른 함수는 그대로 둔다."


@pytest.fixture()
def repo(tmp_path):
    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)
    git("init", "-q")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    (tmp_path / "calc.py").write_text("def sub(a, b):\n    return a + b\n", encoding="utf-8")
    (tmp_path / "big.py").write_text("x = 1\n" * 200, encoding="utf-8")   # 1,200 바이트 → 약 400 토큰
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_calc.py").write_text("def test_sub():\n    pass\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "-m", "init")
    return tmp_path


def test_clean_ticket_has_no_blocks_or_warnings(repo):
    r = w.precheck(TASK, str(repo), None, ["calc.py"], "python -m pytest -q", CFG)
    assert r == {"blocks": [], "warnings": []}


def test_more_than_three_files_is_blocked(repo):
    r = w.precheck(TASK, str(repo), None, ["calc.py", "big.py", "tests/test_calc.py", "calc.py"], "x", CFG)
    assert any("4개" in b for b in r["blocks"])


def test_file_missing_at_ref_is_blocked(repo):
    r = w.precheck(TASK, str(repo), None, ["nope.py"], "x", CFG)
    assert r["blocks"] == ["기준 커밋(HEAD)에 없는 파일: nope.py"]


def test_files_over_half_of_context_are_blocked(repo):
    r = w.precheck(TASK, str(repo), None, ["big.py"], "x", {"ctx": 600})   # 400 토큰 > 600 x 0.5
    assert any("50%" in b for b in r["blocks"])
    assert w.precheck(TASK, str(repo), None, ["big.py"], "x", {"ctx": 1000})["blocks"] == []


def test_url_repo_skips_file_checks():
    r = w.precheck(TASK, "https://example.invalid/r.git", None, ["nope.py"], "x", CFG)
    assert r["blocks"] == []


def test_short_task_and_missing_test_cmd_warn(repo):
    r = w.precheck("고쳐", str(repo), None, ["calc.py"], None, CFG)
    assert r["blocks"] == []
    assert any("짧다(2자)" in x for x in r["warnings"])
    assert any("test_cmd" in x for x in r["warnings"])


@pytest.mark.parametrize("task", ["tests/test_calc.py 에 sub 테스트를 작성하라", "Write tests for sub in calc.py please"])
def test_test_writing_task_warns(repo, task):
    r = w.precheck(task, str(repo), None, ["calc.py"], "x", CFG)
    assert any("테스트 작성" in x for x in r["warnings"])


def test_only_test_files_listed_warns_even_for_implementation(repo):
    # 11-26 R1 에서 본 현재 동작: 구현할 새 파일을 files 에 못 넣고 테스트 파일만 주면 '테스트 작성' 경고가 붙는다.
    r = w.precheck(TASK, str(repo), None, ["tests/test_calc.py"], "x", CFG)
    assert any("테스트 작성" in x for x in r["warnings"])


def test_conductor_words_warn(repo):
    r = w.precheck("calc 모듈 전체 구조를 다시 설계하고 원인 분석까지 해 줘", str(repo), None, ["calc.py"], "x", CFG)
    assert any("지휘자 쪽 일" in x and "설계" in x for x in r["warnings"])


def test_handoff_rules():
    assert w.handoff("done") is None
    h = w.handoff("tests_failed")
    assert h["to"] == "conductor" and "최대 1번" in h["retry_limit"]
    assert w.handoff("weird_status")["next"] == w.HANDOFF_NEXT["error"]
