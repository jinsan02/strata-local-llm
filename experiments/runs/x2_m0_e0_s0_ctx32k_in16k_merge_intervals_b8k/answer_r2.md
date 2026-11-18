구간을 시작 시간 기준 오름차순으로 정렬한 뒤 순회하며, 다음 구간이 이전 구간의 끝점과 겹치거나 맞닿으면(`start <= last_end`) 끝점을 확장하고 그렇지 않으면 새 구간을 추가합니다. `sorted()`와 리스트 복사를 사용하므로 원본 입력은 변경되지 않으며, 시간 복잡도 `O(n log n)`, 공간 복잡도 `O(n)`입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged
```