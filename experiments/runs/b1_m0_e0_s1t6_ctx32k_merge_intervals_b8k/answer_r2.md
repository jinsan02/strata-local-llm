### 설명
1. **정렬**: 시작점(`start`) 기준 오름차순으로 구간을 정렬합니다.
2. **병합 순회**: 정렬된 구간을 순회하며, 현재 구간의 시작점이 이전 병합된 구간의 끝점보다 작거나 같으면(`start <= last_end`) 겹치거나 맞닿은 상태이므로 끝점을 최대값으로 갱신해 병합합니다. 그렇지 않으면 새 구간으로 추가합니다.
3. **입력 보호**: `sorted()`로 새 리스트를 생성하고, 병합 시에도 새로운 내부 리스트를 사용하므로 원본 입력은 절대 변경되지 않습니다.
- 시간복잡도: `O(N log N)` (정렬)
- 공간복잡도: `O(N)` (출력 및 정렬용 복사본)

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작점 기준 정렬 (원본 불변 보장)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [list(sorted_intervals[0])]  # 첫 구간 복사본으로 초기화
    
    for start, end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
            
    return merged
```