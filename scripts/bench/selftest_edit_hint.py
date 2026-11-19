"""H6 edit 힌트 자체 점검 (모델 · 서버 없이). python selftest_edit_hint.py <run_x3.py 폴더>"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import run_x3 as x3  # noqa: E402

SRC = '''class Version:
    def __repr__(self) -> str:
        return f"<Version({str(self)!r})>"

    def __str__(self) -> str:
        parts = []
        return "".join(parts)


def _parse(x):
    return x
'''


def main() -> int:
    d = Path(tempfile.mkdtemp())
    try:
        (d / "pkg").mkdir()
        f = d / "pkg" / "v.py"
        f.write_text(SRC, encoding="utf-8", newline="\n")
        bad = {"path": "pkg/v.py", "old_string": "  def __str__(self) -> str:\n      parts = []", "new_string": "X"}   # 들여쓰기 틀림
        fails = []
        x3.EDIT_HINT = False
        ok, out_off = x3.edit_file(d, bad, ())
        c1 = not ok and "가장 비슷한" not in out_off and out_off.endswith("그대로 복사하라")
        x3.EDIT_HINT = True
        ok, out_on = x3.edit_file(d, bad, ())
        c2 = (not ok and "가장 비슷한 현재 원문" in out_on and "    def __str__(self) -> str:\n        parts = []" in out_on
              and "   5" not in out_on)
        ok, out_none = x3.edit_file(d, {"path": "pkg/v.py", "old_string": "zzzz qqqq totally different", "new_string": "X"}, ())
        c3 = not ok and "가장 비슷한" not in out_none
        dup = {"path": "pkg/v.py", "old_string": "        return", "new_string": "X"}   # 2회 일치: 힌트 없음
        ok, out_dup = x3.edit_file(d, dup, ())
        c4 = not ok and "2회" in out_dup and "가장 비슷한" not in out_dup
        good = {"path": "pkg/v.py", "old_string": "        parts = []\n", "new_string": "        parts = ['a']\n"}
        ok, _ = x3.edit_file(d, good, ())
        c5 = ok and "parts = ['a']" in f.read_text(encoding="utf-8")
        x3.EDIT_HINT = False
        for name, c in (("off=H0 메시지", c1), ("on 힌트(공백 그대로 · 줄 번호 없음)", c2), ("비슷한 것 없음", c3), ("2회 일치엔 힌트 없음", c4), ("정상 편집", c5)):
            print(name, c)
            if not c:
                fails.append(name)
        print("--- on 메시지 ---\n" + out_on)
        print("FAIL", fails or "없음 — 전부 통과")
        return 1 if fails else 0
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
