### 설명
1. 입력 리스트가 비었으면 즉시 빈 리스트를 반환합니다.
2. 원본을 보호하기 위해 구간을 시작점(`x[0]`) 기준으로 정렬한 **사본**을 생성합니다.
3. 정렬된 구간을 앞에서부터 순회하며, 현재 구간의 시작점이 `마지막으로 합친 구간의 끝점`보다 작거나 같으면(겹치거나 맞닿음) 끝값을 두 값 중 큰 것으로 업데이트하여 병합합니다. 그렇지 않으면 새 구간으로 추가합니다.
4. 정렬된 상태로 탐색하므로 결과 리스트는 자연스럽게 시작점 오름차순이 유지되며, 모든 새 리스트 객체를 생성해 입력 원본에 영향을 주지 않습니다. 시간 복잡도 `O(N log N)`, 공간 복잡도 `O(N)`입니다.

### 코드
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 시작점 기준으로 정렬된 사본을 생성하여 원본 수정을 방지합니다.
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [[sorted_intervals[0][0], sorted_intervals[0][1]]]
    for start, end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        # 겹치거나 맞닿은 경우 병합 (끝값 최대화)
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
            
    return merged
```