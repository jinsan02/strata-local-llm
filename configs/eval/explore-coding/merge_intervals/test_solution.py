from solution import merge_intervals


def test_basic():
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_touching():
    assert merge_intervals([[1, 3], [3, 5]]) == [[1, 5]]


def test_unsorted_and_nested():
    assert merge_intervals([[5, 7], [1, 10], [2, 3]]) == [[1, 10]]


def test_empty():
    assert merge_intervals([]) == []


def test_not_mutated():
    data = [[3, 4], [1, 2]]
    merge_intervals(data)
    assert data == [[3, 4], [1, 2]]


def test_single_points():
    assert merge_intervals([[4, 4], [1, 1], [1, 2]]) == [[1, 2], [4, 4]]
