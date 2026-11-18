import json

import pytest

from solution import KVStore


class Clock:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def test_set_get_delete():
    s = KVStore(clock=Clock())
    s.set("a", 1)
    assert s.get("a") == 1
    assert s.get("b", "x") == "x"
    assert s.delete("a") is True
    assert s.delete("a") is False
    assert s.get("a") is None


def test_ttl_expiry_and_reset():
    c = Clock()
    s = KVStore(clock=c)
    s.set("a", 1, ttl=5)
    c.t = 104.9
    assert s.get("a") == 1
    c.t = 105.0
    assert s.get("a") is None
    s.set("b", 2, ttl=1)
    s.set("b", 3)
    c.t = 200.0
    assert s.get("b") == 3


def test_keys_prefix_sorted_and_live_only():
    c = Clock()
    s = KVStore(clock=c)
    for k in ["user:b", "user:a", "item:1", "user:c"]:
        s.set(k, 0)
    s.set("user:z", 0, ttl=1)
    c.t = 101.0
    assert s.keys("user:") == ["user:a", "user:b", "user:c"]
    assert s.keys() == ["item:1", "user:a", "user:b", "user:c"]


def test_transaction_commit():
    s = KVStore(clock=Clock())
    s.set("a", 1)
    s.begin()
    s.set("a", 2)
    s.set("b", 3)
    assert s.get("a") == 2
    s.commit()
    assert s.get("a") == 2 and s.get("b") == 3


def test_transaction_rollback_and_delete_visibility():
    s = KVStore(clock=Clock())
    s.set("a", 1)
    s.begin()
    s.delete("a")
    assert s.get("a") is None
    assert s.keys() == []
    s.rollback()
    assert s.get("a") == 1


def test_nested_transactions():
    s = KVStore(clock=Clock())
    s.set("a", 1)
    s.begin()
    s.set("a", 2)
    s.begin()
    s.set("a", 3)
    assert s.get("a") == 3
    s.rollback()
    assert s.get("a") == 2
    s.begin()
    s.set("c", 9)
    s.commit()
    assert s.get("c") == 9
    s.rollback()
    assert s.get("a") == 1
    assert s.get("c") is None


def test_commit_rollback_without_transaction():
    s = KVStore(clock=Clock())
    with pytest.raises(RuntimeError):
        s.commit()
    with pytest.raises(RuntimeError):
        s.rollback()


def test_snapshot_excludes_open_transaction():
    s = KVStore(clock=Clock())
    s.set("a", 1)
    s.begin()
    s.set("b", 2)
    data = json.loads(s.snapshot()) if isinstance(s.snapshot(), str) else None
    assert data is not None
    r = KVStore.restore(s.snapshot(), clock=Clock())
    assert r.get("a") == 1
    assert r.get("b") is None


def test_snapshot_restore_ttl_remaining():
    c = Clock()
    s = KVStore(clock=c)
    s.set("a", {"x": [1, 2]}, ttl=10)
    s.set("p", "keep")
    c.t = 104.0
    snap = s.snapshot()
    c2 = Clock()
    c2.t = 1000.0
    r = KVStore.restore(snap, clock=c2)
    assert r.get("a") == {"x": [1, 2]}
    c2.t = 1005.9
    assert r.get("a") == {"x": [1, 2]}
    c2.t = 1006.0
    assert r.get("a") is None
    assert r.get("p") == "keep"


def test_snapshot_drops_expired():
    c = Clock()
    s = KVStore(clock=c)
    s.set("a", 1, ttl=1)
    c.t = 102.0
    r = KVStore.restore(s.snapshot(), clock=Clock())
    assert r.keys() == []


def test_stats():
    s = KVStore(clock=Clock())
    s.set("a", 1)
    s.set("b", 2)
    s.delete("a")
    s.delete("zzz")
    s.begin()
    s.set("c", 3)
    st = s.stats()
    assert st["sets"] == 3
    assert st["deletes"] == 1
    assert st["depth"] == 1
    assert st["keys"] == 1


def test_default_clock_works():
    s = KVStore()
    s.set("a", 1, ttl=1000)
    assert s.get("a") == 1
