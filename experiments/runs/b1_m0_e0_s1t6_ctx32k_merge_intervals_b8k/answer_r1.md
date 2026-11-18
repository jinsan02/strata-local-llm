### 설명
1. 입력이 비어있으면 바로 빈 리스트를 반환합니다.
2. `sorted()` 로 시작 시간을 기준으로 정렬된 **새 리스트**를 생성하여 원본 데이터가 변경되지 않도록 합니다.
3. 정렬된 구간을 순회하며, 마지막 병합 구간의 끝값(`end`)과 현재 구간의 시작값(`start`)을 비교합니다.
4. `current_start <= last_end`이면 겹치거나 맞닿은 상태이므로, 두 구간의 끝값 중 큰 값으로 업데이트하여 합칩니다. 조건이 만족되지 않으면 새로운 구간으로 추가합니다.
5. 초기 정렬과 병합 순서 덕분에 결과물은 자연스럽게 시작점 오름차순을 유지합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 원본 수정 방지를 위해 정렬된 새 리스트 생성
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    
    for curr in sorted_intervals[1:]:
        last = merged[-1]
        # 겹치거나 맞닿은 경우 병합 (end 값 확장)
        if curr[0] <= last[1]:
            last[1] = max(last[1], curr[1])
        else:
            merged.append(curr)
            
    return merged
```