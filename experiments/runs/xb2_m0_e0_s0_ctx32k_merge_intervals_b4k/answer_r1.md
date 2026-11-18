### 핵심 논리
1. `sorted()`로 시작점 기준 정렬된 **새로운 리스트**를 만들어 원본을 보호합니다.
2. 첫 구간을 `current`로 설정한 후 나머지 구간과 순회 비교합니다.
3. 다음 구간의 시작점이 `current.end`보다 작거나 같으면(겹침 or 접합) 끝점을 확장하고, 아니면 현재 구간을 결과에 추가해 새 구간으로 넘어갑니다.
4. 시간복잡도: `O(n log n)` (정렬), 공간복잡도: `O(n)` (출력 리스트 및 정렬 복사본).

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 원본 변경 방지 및 시작점 기준 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged = []
    curr_start, curr_end = sorted_intervals[0]

    for next_start, next_end in sorted_intervals[1:]:
        if next_start <= curr_end:  # 겹치거나 맞닿은 경우 병합
            curr_end = max(curr_end, next_end)
        else:
            merged.append([curr_start, curr_end])
            curr_start, curr_end = next_start, next_end

    merged.append([curr_start, curr_end])
    return merged
```