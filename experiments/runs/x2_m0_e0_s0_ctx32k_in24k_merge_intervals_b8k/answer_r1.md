### 알고리즘 개요
1. **정렬**: 입력 구간을 시작값(`start`)을 기준으로 정렬합니다. Python의 `sorted()`는 안정 정렬이며 새 리스트를 반환하므로 원본을 건드리지 않습니다.
2. **단일 순회 병합**: 정렬된 구간을 앞에서부터 훑으며 마지막 결과 구간과 비교합니다. 현재 구간의 시작값이 마지막 결과 구간의 끝값보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로 끝값을 더 큰 값으로 업데이트하고, 그렇지 않으면 새 구간으로 추가합니다.
3. **참조 분리**: 병합 과정에서 새 리스트를 할당하거나 생성해 원본 및 정렬된 내부 배열에 대한 변조를 원천 차단합니다.

시간 복잡도: `O(N log N)` (정렬), 공간 복잡도: `O(N)` (출력용).

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작 시간을 기준으로 정렬 (원본 리스트는 복사/변경되지 않음)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for curr_start, curr_end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if curr_start <= last_end:  # 겹치거나 맞닿는 경우 병합
            merged[-1] = [last_start, max(last_end, curr_end)]
        else:
            merged.append([curr_start, curr_end])

    return merged
```