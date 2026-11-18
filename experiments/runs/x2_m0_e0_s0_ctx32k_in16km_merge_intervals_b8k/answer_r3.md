간단한 정렬 후 단일 라인 스캔(linear scan) 방식으로 해결합니다. 입력 리스트의 참조를 유지하지 않도록 내부를 복제하여 생성하고, 시작점 오름차순 기준으로 정렬한 뒤 겹침/맞닿음 조건(`current_start <= last_end`)이 성립할 때 끝점을 확장하여 병합합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 시작점 오름차순, 같으면 끝점 내림차순 정렬 (병합 효율성 향상)
    sorted_ints = sorted(intervals, key=lambda x: (x[0], -x[1]))
    
    # 새 리스트를 만들어 원본을 변경하지 않음
    merged = [list(sorted_ints[0])]
    for start, end in sorted_ints[1:]:
        if start <= merged[-1][1]:  # 겹치거나 맞닿은 경우
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
            
    return merged
```