### 동작 방식
1. 입력이 비어 있으면 즉시 빈 리스트를 반환합니다.
2. 원본 데이터를 건드리지 않기 위해 `sorted()` 로 시작 시간 기준 복사 정렬을 수행합니다.
3. 정렬된 구간의 첫 번째를 결과 리스트에 초기화한 뒤, 나머지 구간을 순회합니다.
4. 현재 구간의 시작점이 직전 구간의 종료점보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로 `max()` 로 종료점을 확장하고, 다르면 새로운 구간으로 추가합니다.
5. 정렬된 순서대로 처리하므로 결과 리스트는 자연스럽게 시작점 오름차순이 됩니다. 시간/공간 복잡도는 각각 `O(N log N)`, `O(N)` 입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작 시간 기준 정렬 (원본 리스트 변경 방지)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [list(sorted_intervals[0])]
    for current in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if current[0] <= last_end:          # 겹치거나 맞닿은 경우
            merged[-1][1] = max(last_end, current[1])
        else:                               # 분리된 경우
            merged.append([current[0], current[1]])
            
    return merged
```