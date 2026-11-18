### 설명
1. 입력이 비어있으면 즉시 `[]`를 반환합니다.
2. 원본 리스트 변경을 피하기 위해 `sorted()`로 새 정렬 결과를 만들고, 결과 목록에 새로운 `[start, end]` 리스트 객체를 할당합니다.
3. 시작점 기준 오름차순으로 정렬한 후 순회하며, 다음 구간의 시작점이 이전 병합 구간의 끝점보다 작거나 같으면(`start <= last_end`) 끝점을 `max(last_end, end)`로 확장합니다.
4. 아니면 새 구간으로 추가합니다. 결과적으로 시작점 기준 오름차순 정렬된 새 리스트가 반환됩니다.
- **시간 복잡도**: O(N log N) (정렬 주도), 병합 스캔 O(N)
- **공간 복잡도**: O(N) (정렬 및 새 결과 리스트 생성)

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 원본을 건드리지 않고 시작점 기준으로 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    # 첫 구간을 새로운 리스트로 초기화
    merged = [[sorted_intervals[0][0], sorted_intervals[0][1]]]

    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged
```