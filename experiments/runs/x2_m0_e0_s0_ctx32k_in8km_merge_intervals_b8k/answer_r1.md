구간을 시작점을 기준으로 정렬한 후, 현재까지의 마지막 구간과 겹치거나 맞닿는 경우 끝점을 확장하여 통합하고, 그렇지 않으면 새 구간으로 추가하는 방식입니다. `sorted()`로 복사 정렬하고 새 리스트를 반환하여 원본 입력을 보호합니다. 시간 복잡도 `O(N log N)`, 공간 복잡도 `O(N)`입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작점 기준으로 정렬 (입력 원본은 변경되지 않음)
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    merged = [sorted_intervals[0].copy()]
    
    for start, end in sorted_intervals[1:]:
        _, last_end = merged[-1]
        # 겹치거나 맞닿은 경우(end <= start) 끝점 통합
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
            
    return merged
```