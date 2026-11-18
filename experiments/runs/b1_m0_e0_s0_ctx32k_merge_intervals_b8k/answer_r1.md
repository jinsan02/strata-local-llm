구간을 시작점 기준으로 정렬한 후, 결과 리스트의 마지막 구간과 현재 구간이 겹치거나 맞닿으면 `max`로 끝점을 확장하고, 아니면 새로운 구간으로 추가하는 그리디 방식을 사용합니다. 원본 입력의 참조를 직접 건드리지 않도록 매 구간을 새 리스트 `[start, end]`로 생성하여 저장합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    merged = []
    for start, end in sorted(intervals, key=lambda x: x[0]):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
            
    return merged
```