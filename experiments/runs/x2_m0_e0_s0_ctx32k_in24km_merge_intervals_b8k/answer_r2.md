### 해설
1. 빈 입력인 경우 즉시 `[]` 를 반환합니다.
2. 시작 값을 기준으로 정렬하되, `sorted()` 로 **새 리스트**를 만들어 원본 참조를 건드리지 않습니다.
3. 정렬된 구간을 순회하며, 현재 구간의 시작점이 이전 구간의 끝점보다 작거나 같으면 겹치거나 맞닿은 것으로 간주해 이전 끝점을 최대값으로 확장합니다.
4. 그렇지 않으면 `[current_start, current_end]` 형식의 **새 리스트**를 결과에 추가합니다. 이 방식은 원본 하위 리스트의 가변성을 보호하며, 최종 반환 리스트는 시작점 오름차순 정렬 상태가 자연스럽게 유지됩니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    sorted_ivs = sorted(intervals, key=lambda x: x[0])
    merged: list[list[int]] = []
    
    for iv in sorted_ivs:
        # 이전 구간 끝보다 현재 구간 시작점이 크면(겹치거나 접하지 않으면) 새 구간으로 추가
        if not merged or merged[-1][1] < iv[0]:
            merged.append([iv[0], iv[1]])
        else:
            # 겹치거나 맞닿으면 이전 끝점을 최대값으로 확장
            merged[-1][1] = max(merged[-1][1], iv[1])
            
    return merged
```