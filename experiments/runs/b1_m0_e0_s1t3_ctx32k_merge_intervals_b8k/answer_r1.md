정렬된 구간을 순회하며 현재 구간이 마지막 합성 구간의 끝점보다 작거나 같으면(겹치거나 맞닿음) 끝점을 최대값으로 확장하고, 그렇지 않으면 새 구간으로 추가하는 그리디 방식으로 구현합니다. 원본 변경 방지를 위해 `sorted()`로 복사 정렬 후 처리하며, 시간복잡도 `O(N log N)`, 공간복잡도 `O(N)`입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작점 기준 오름차순 정렬 (원본 리스트는 변경되지 않음)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    
    for current in sorted_intervals[1:]:
        # 겹치거나 맞닿은 경우 끝점을 최대값으로 확장
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            # 분리된 경우 새 구간으로 추가
            merged.append(current)
            
    return merged
```