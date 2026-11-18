### 설명
입력 구간을 시작점 기준으로 정렬한 후 순회하며 병합합니다. 현재 구간의 시작점이 이전 결과 구간의 끝보다 작거나 같으면(겹치거나 맞닿음) 끝점을 `max`로 확장하고, 다르면 새로운 구간으로 추가합니다. 원본 변경 방지를 위해 정렬 시 사본을 생성하고 결과 리스트에도 새 리스트 객체로 저장합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작점 기준 정렬 (원본 데이터는 건드리지 않음)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]
    
    for s, e in sorted_intervals[1:]:
        last_end = merged[-1][1]
        if s <= last_end:
            # 겹치거나 맞닿으면 끝점 확장
            merged[-1][1] = max(last_end, e)
        else:
            # 그렇지 않으면 새 구간 추가 (사본 생성으로 원본 보호)
            merged.append([s, e])
            
    return merged
```