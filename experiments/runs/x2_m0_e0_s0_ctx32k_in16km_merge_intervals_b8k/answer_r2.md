### 설명
1. 빈 입력일 경우 바로 빈 리스트를 반환합니다.
2. 원본 데이터를 변경하지 않도록, 시작점을 기준으로 정렬한 사본을 생성합니다.
3. 첫 번째 구간을 결과 리스트(`merged`)에 초기화합니다.
4. 정렬된 구간들을 순회하며, 현재 구간의 시작점이 이전 구간의 끝점보다 작거나 같으면(겹치거나 맞닿는 경우) 이전 구간의 끝점을 두 구간의 최댓값으로 갱신합니다. 그렇지 않으면 새로운 구간을 추가합니다.
5. 최종적으로 병합되고 정렬된 새 리스트를 반환합니다. 시간 복잡도: `O(n log n)` (정렬 기준), 공간 복잡도: `O(n)`.

### 최종 코드
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 원본 리스트 변경 방지를 위해 시작점 기준으로 정렬한 사본 생성
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [[sorted_intervals[0][0], sorted_intervals[0][1]]]
    
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  # 겹치거나 맞닿은 경우 병합
            last[1] = max(last[1], current[1])
        else:                      # 그렇지 않으면 새 구간 추가
            merged.append([current[0], current[1]])
            
    return merged
```