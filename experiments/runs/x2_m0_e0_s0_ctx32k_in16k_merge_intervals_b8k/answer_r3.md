### 설명
1. 입력이 비어있으면 즉시 `[]`를 반환합니다.
2. 원본 리스트를 변경하지 않기 위해 `sorted()`로 시작 시간을 기준으로 정렬된 새 객체를 생성합니다.
3. 정렬된 구간을 순회하며, 현재 구간의 시작점이 결과 리스트의 마지막 구간 끝점보다 작거나 같으면(`start <= last_end`) 두 끝점 중 큰 값으로 확장(병합)합니다. 예시의 `[1,3]`과 `[3,5]`가 맞닿는 경우를 포함하여 처리합니다.
4. 맞물리지 않으면 새 구간으로 추가하고, 최종적으로 새로운 리스트를 반환합니다. 시간 복잡도 `O(N log N)` (정렬 기준), 공간 복잡도 `O(N)`.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 원본 보호: 시작 시간을 기준으로 정렬된 복사본 생성
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    # 첫 번째 구간의 복사본으로 결과 초기화
    merged = [list(sorted_intervals[0])]
    
    for start, end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:  # 겹치거나 끝점-시작점이 맞닿는 경우 (포함 경계)
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
            
    return merged
```