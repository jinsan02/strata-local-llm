### 설명
1. 입력이 비어있으면 빈 리스트를 즉시 반환합니다.
2. 원본 내보트나 내부 요소를 수정하지 않도록 `sorted()`로 시작점 기준 정렬된 복사본을 만듭니다.
3. 정렬된 구간을 순회하며 마지막 병합된 구간의 끝점과 비교합니다. 현재 구간의 시작점이 이전 끝점 이하이면(중복 또는 맞닿음) 끝점을 두 값 중 큰 것으로 확장하고, 그렇지 않으면 새 구간으로 추가합니다.
4. 전체 시간 복잡도는 `O(n log n)` (정렬), 공간 복잡도는 `O(n)` 입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 원본 수정 방지 & 시작점 오름차순 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0][:]]  # 첫 구간 복사본으로 초기화
    
    for current in sorted_intervals[1:]:
        last = merged[-1]
        # 겹치거나 맞닿은 경우 끝점 확장 (inclusion 기준)
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current[:])  # 새 구간 복사본 추가
            
    return merged
```