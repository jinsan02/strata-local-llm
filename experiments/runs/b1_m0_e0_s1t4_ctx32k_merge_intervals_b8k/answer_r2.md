### 설명
1. 빈 입력인 경우 즉시 빈 리스트를 반환합니다.
2. `sorted()`를 사용해 시작점을 기준으로 정렬된 **새로운 리스트**를 생성하여 원본을 건드리지 않습니다.
3. 정렬된 구간을 순회하며, 앞선 구간의 끝점과 현재 구간의 시작점이 겹치거나 맞닿는 경우(`current[0] <= last_end`) 최대 끝점으로 확장하고, 아니면 새 구간으로 추가합니다.
- 시간 복잡도: `O(N log N)` (정렬)
- 공간 복잡도: `O(N)` (결과 리스트 및 정렬 복사본)

### 코드
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 원본을 변경하지 않으면서 시작점 기준 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:  # 겹치거나 맞닿음
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
            
    return merged
```