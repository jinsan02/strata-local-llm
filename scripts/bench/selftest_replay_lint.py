import sys; sys.path.insert(0, r"C:\strata-lab\work\stage")
from replay_lint import static_issues as S
cases = {
 "undef":      ("def f():\n    return foo + 1\n", {"undefined name 'foo'"}),
 "ok_param":   ("import os\nX = 1\ndef f(a):\n    return a + X + len(os.sep)\n", set()),
 "closure":    ("def f():\n    y = 1\n    def g():\n        return y\n    return g\n", set()),
 "comp":       ("def f(xs):\n    return [x*2 for x in xs if x]\n", set()),
 "class_attr": ("class A:\n    K = 1\n    def m(self):\n        return K\n", {"undefined name 'K'"}),
 "global_def": ("def f():\n    global Z\n    Z = 1\ndef g():\n    return Z\n", set()),
 "try_import": ("try:\n    import json as j\nexcept ImportError:\n    j = None\ndef f():\n    return j\n", set()),
 "late_def":   ("def f():\n    return later()\ndef later():\n    return 1\n", set()),
 "syntax":     ("def f(:\n  pass\n", None),
 "typing":     ("from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from x import Y\ndef f(a: 'Y') -> None:\n    return None\n", set()),
 "self_meth":  ("class A:\n    def m(self):\n        return self.n()\n", set()),
 "walrus":     ("def f(xs):\n    if (n := len(xs)) > 1:\n        return n\n", set()),
 "except_as":  ("def f():\n    try:\n        pass\n    except Exception as e:\n        return e\n", set()),
}
bad = 0
for k, (src, want) in cases.items():
    got = S(src, k)
    ok = (got and all(x.startswith("syntax") for x in got)) if want is None else got == want
    print("ok " if ok else "FAIL", k, got); bad += not ok
print("FAIL 0" if not bad else f"FAIL {bad}")
