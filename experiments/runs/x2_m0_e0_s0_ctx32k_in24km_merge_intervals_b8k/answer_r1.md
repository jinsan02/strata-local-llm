구간을 시작점을 기준으로 정렬한 뒤 순회하며 병합합니다. 이전 구간의 끝점(`last_end`)보다 현재 구간의 시작점이 작거나 같으면(`start <= last_end`) 겹치거나 맞닿은 것이므로 마지막 구간의 끝점을 최대값으로 업데이트하고, 그렇지 않으면 새 구간을 추가합니다. `sorted()`가 새 리스트를 반환하므로 원본 입력 리스트는 변경되지 않습니다.

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