입력 리스트를 `start` 기준 정렬한 복사본을 만든 후, 첫 구간을 결과 리스트에 초기화합니다. 순회하며 현재 구간의 시작점이 마지막 결과 구간의 끝점보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로 끝점을 최대값으로 업데이트하여 병합하고, 그렇지 않으면 새로운 구간으로 추가합니다. `sorted()`를 사용해 원본 입력을 변조하지 않으며, 중복 정렬이나 추가 라이브러리 없이 O(N log N) 시간 복잡도로 동작합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 원본 입력을 변경하지 않기 위해 새로 정렬된 리스트 생성
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
            
    return merged
```