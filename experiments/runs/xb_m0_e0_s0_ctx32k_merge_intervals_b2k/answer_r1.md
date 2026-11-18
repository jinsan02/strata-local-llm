알고리즘은 다음과 같습니다:
1. 입력이 비어있다면 즉시 빈 리스트를 반환합니다.
2. 원본 리스트를 보호하기 위해 `sorted()`로 시작점 기준 정렬된 새 리스트를 생성합니다.
3. 첫 정렬된 구간의 복사본을 결과 리스트에 초기화합니다.
4. 나머지 구간을 순회하며, 현재 구간의 시작점이 결과 리스트의 마지막 구간 끝값보다 작거나 같으면 `max`로 끝값을 확장해 병합합니다. 다르면 새로운 구간으로 추가합니다.
5. 정렬 조건과 불변성을 모두 만족하므로 최종 리스트를 반환합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 원본 수정 방지를 위해 정렬된 새 리스트 생성 (시작점 기준)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [list(sorted_intervals[0])]  # 첫 구간 복사본으로 초기화
    
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        
        # 겹치거나 맞닿은 경우 병합
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
            
    return merged
```