import pytest

from solution import topo_sort


def test_simple():
    assert topo_sort({"b": ["a"], "c": ["b"]}) == ["a", "b", "c"]


def test_lexicographic_ties():
    assert topo_sort({"d": ["b", "a"], "c": []}) == ["a", "b", "c", "d"]


def test_nodes_only_in_lists():
    assert topo_sort({"x": ["z", "y"]}) == ["y", "z", "x"]


def test_cycle():
    with pytest.raises(ValueError):
        topo_sort({"a": ["b"], "b": ["a"]})


def test_self_cycle():
    with pytest.raises(ValueError):
        topo_sort({"a": ["a"]})


def test_empty():
    assert topo_sort({}) == []
