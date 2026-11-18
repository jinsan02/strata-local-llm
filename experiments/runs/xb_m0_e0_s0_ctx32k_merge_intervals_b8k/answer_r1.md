### 설명
1. 입력이 비었으면 빈 리스트를 반환합니다.
2. 원본 데이터를 보존하기 위해 `sorted()`로 시작점 기준 정렬된 복사본을 생성합니다.
3. 첫 번째 구간을 결과 리스트에 초기화한 후, 나머지를 순회하며 **현재 구간의 시작점이 이전 구간의 끝점보다 작거나 같으면**(겹치거나 맞닿는 경우) 끝점을 최대값으로 확장하고, 그렇지 않으면 새로운 구간으로 추가합니다.
4. 모든 처리 후 정렬된 새 리스트를 반환합니다.

### 코드
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 원본 수정 방지 및 시작점 기준 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [list(sorted_intervals[0])]
    for start, end in sorted_intervals[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(prev_end, end)
        else:
            merged.append([start, end])
            
    return merged
```