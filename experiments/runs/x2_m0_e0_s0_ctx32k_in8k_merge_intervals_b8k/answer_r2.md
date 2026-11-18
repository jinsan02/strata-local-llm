### 설명
1. **빈 입력 처리**: 입력이 비어있으면 즉시 빈 리스트를 반환합니다.
2. **정렬 및 복사**: `sorted()`로 시작점 기준 오름차순 정렬된 **새로운 리스트**를 생성해 원본 수정을 방지합니다.
3. **병합 순회**: 정렬된 구간을 순회하며 결과 리스트의 마지막 구간과 비교합니다.
   - 현재 구간의 시작점이 마지막 구간의 끝점보다 작거나 같으면(`start <= last_end`), 겹치거나 맞닿은 것이므로 마지막 구간의 끝점을 두 끝점의 최댓값으로 확장합니다.
   - 그렇지 않으면 독립된 구간이므로 새로운 리스트로 추가합니다.
4. **복잡도**: 시간 `O(N log N)` (정렬 주도), 공간 `O(N)` (새 결과 리스트 저장).

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    sorted_ints = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_ints[0])]
    
    for start, end in sorted_ints[1:]:
        if start <= merged[-1][1]:  # 겹치거나 맞닿은 경우 (예: [1,3]과 [3,5])
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
            
    return merged
```