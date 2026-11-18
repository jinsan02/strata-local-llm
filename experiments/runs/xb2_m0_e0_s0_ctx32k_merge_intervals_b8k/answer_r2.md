### 알고리즘 설명
1. 입력이 빈 리스트면 즉시 `[]` 반환.
2. 구간을 **시작 시간 기준 오름차순**으로 정렬합니다 (`sorted()` 사용).
3. 결과 리스트(`merged`)에 정렬된 첫 번째 구간의 복사본을 추가합니다.
4. 나머지 정렬된 구간들을 순회하며, 현재 시작점이 `merged`의 마지막 구간 끝값보다 작거나 같으면(겹치거나 맞닿음) 최대 끝값으로 갱신하고, 다르면 새로운 구간으로 추가합니다.
5. 입력 원본 내부 리스트까지 변경되는 것을 방지하기 위해 슬라이싱(`[:]`)으로 복사본을 사용합니다.

**복잡도**: 시간 `O(N log N)` (정렬), 공간 `O(N)` (출력 및 정렬용 임시 리스트)

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작 시간을 기준으로 정렬 (입력 원본은 변경되지 않음)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [sorted_intervals[0][:]]  # 첫 구간 복사본으로 초기화
    
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(last_end, end)
        else:                  # 겹치지 않는 경우 별도 구간으로 추가
            merged.append([start, end])
            
    return merged
```