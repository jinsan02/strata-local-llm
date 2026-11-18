### 설명
1. 빈 입력이면 즉시 `[]`를 반환합니다.
2. 원본 리스트의 순서나 요소를 보호하기 위해 `sorted()`로 **시작점을 기준으로 정렬한 새 리스트**를 생성합니다.
3. 정렬된 구간의 첫 번째를 결과 리스트에 추가한 뒤, 나머지와 순회하며 비교합니다.
4. 현재 구간의 시작점이 직전 병합 구간의 끝점보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로 `max()`로 끝점을 확장해 병합합니다.
5. 그렇지 않으면 별도 구간으로 추가합니다.
6. 정렬 순서대로 처리하므로 결과 리스트는 자연스럽게 시작점 오름차순을 유지하며 새 리스트를 반환합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 원본 수정 방지를 위해 정렬된 복사본 생성 (시작점, 끝점 기준)
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    
    merged = [sorted_intervals[0]]
    for curr in sorted_intervals[1:]:
        # 겹치거나 맞닿은 경우 병합
        if curr[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], curr[1])
        else:
            merged.append(curr)
            
    return merged
```