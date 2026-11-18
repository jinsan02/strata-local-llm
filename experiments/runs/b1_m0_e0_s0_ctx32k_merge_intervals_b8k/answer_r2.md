### 설명
1. 입력이 비면 바로 빈 리스트를 반환합니다.
2. `sorted()`로 시작점을 기준으로 정렬된 **새 리스트**를 만들어 원본 데이터가 변경되지 않도록 보호합니다.
3. 첫 구간의 복사본을 결과 리스트에 추가한 후, 나머지 구간을 순회합니다.
4. 현재 구간의 시작점이 이전 결과 구간의 끝점보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로 이전 구간의 끝점을 `max`로 확장하여 병합합니다. 그렇지 않으면 새 구간으로 추가합니다.
5. 시간 복잡도: `O(N log N)` (정렬), 공간 복잡도: `O(N)` (결과 리스트 및 정렬 복사본).

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 원본 보호를 위해 시작점 기준 정렬된 새 리스트 생성
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]  # 첫 구간 복사
    
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
            
    return merged
```