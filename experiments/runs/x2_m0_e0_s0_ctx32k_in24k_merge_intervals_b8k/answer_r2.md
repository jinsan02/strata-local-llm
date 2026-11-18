알고리즘은 다음과 같습니다:
1. 시작 시간 기준으로 구간의 순서를 정렬합니다 (`sorted`는 새 리스트를 반환하므로 원본이 유지됨).
2. 정렬된 구간을 순회하며, 현재 구간의 시작점이 직전 결과 구간의 끝점과 겹치거나 같으면(`start <= last_end`) 끝점을 `max()`로 확장합니다.
3. 겹치지 않으면 새로운 구간으로 추가합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작점 기준 정렬 (원본 outer list 변경 안됨)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]  # 첫 구간 복사하여 초기화
    
    for start, end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:               # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(last_end, end)
        else:                               # 구간이 분리된 경우 추가
            merged.append([start, end])
            
    return merged
```