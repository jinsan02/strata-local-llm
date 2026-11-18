입력 구간을 시작점을 기준으로 정렬한 후, 앞선 구간의 끝점과 현재 구간의 시작점이 겹치거나 닿으면(`start <= last_end`) 끝점을 최댓값으로 확장하고, 그렇지 않으면 새 구간으로 추가합니다. 입력 원본의 수정을 방지하기 위해 정렬 및 슬라이싱 과정을 통해 완전한 새 리스트를 반환합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 시작점을 기준으로 정렬된 복사본 생성 (원본 불변 보장)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0][:]]
    
    for curr in sorted_intervals[1:]:
        # 겹치거나 맞닿으면 끝점을 확장, 아니면 새 구간 추가
        if curr[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], curr[1])
        else:
            merged.append(curr[:])
            
    return merged
```