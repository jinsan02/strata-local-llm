from solution import LRUCache


def test_basic_eviction():
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


def test_update_refreshes():
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2); c.put(1, 10)
    c.put(3, 3)
    assert c.get(1) == 10
    assert c.get(2) == -1


def test_zero_capacity():
    c = LRUCache(0)
    c.put(1, 1)
    assert c.get(1) == -1


def test_missing():
    assert LRUCache(1).get(42) == -1


def test_many_ops_fast():
    c = LRUCache(1000)
    for i in range(200_000):
        c.put(i, i)
        c.get(i - 500)
    assert c.get(199_999) == 199_999
