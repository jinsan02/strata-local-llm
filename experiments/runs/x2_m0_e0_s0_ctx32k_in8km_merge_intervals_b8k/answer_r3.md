입력 리스트를 시작점 기준으로 정렬한 뒤, 첫 번째 구간을 복사하여 결과 목록에 추가합니다. 이후 구간을 순회하며 시작점이 이전 구간의 끝점보다 작거나 같으면 끝점을 최댓값으로 확장해 병합하고, 그렇지 않으면 새 구간을 복사하여 추가합니다. 이 방식은 원본 리스트를 건드리지 않으면서 $O(N \log N)$ 시간 내에 해결합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 시작점을 기준으로 정렬한 새 리스트를 만들어 원본을 보호합니다.
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    merged = [sorted_intervals[0][:]]
    
    for interval in sorted_intervals[1:]:
        last = merged[-1]
        # 겹치거나 맞닿은 경우 끝점을 확장하여 병합
        if interval[0] <= last[1]:
            last[1] = max(last[1], interval[1])
        else:
            # 다음 구간이므로 복사하여 추가
            merged.append(interval[:])
            
    return merged
```