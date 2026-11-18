이 문제는 **정렬 후 단방향 스캔**으로 해결합니다.

1. 구간을 시작점(`start`) 기준으로 정렬합니다. (`sorted()`는 새 리스트를 반환하므로 원본은 변경되지 않습니다.)
2. 첫 번째 구간을 복사해 결과 리스트에 초기화합니다.
3. 순회하며 현재 구간의 시작점이 마지막 결과 구간의 끝점보다 작거나 같으면(겹치거나 맞닿음) 끝점을 `max`로 확장합니다. 그렇지 않으면 새로운 구간으로 추가합니다.
4. 정렬된 순서대로 처리하므로 결과 리스트는 자연스럽게 시작점 오름차순이 됩니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작점 기준 정렬 (원본 리스트 변경 없음)
    sorted_ints = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_ints[0].copy()]

    for curr in sorted_ints[1:]:
        last = merged[-1]
        if curr[0] <= last[1]:  # 겹치거나 맞닿음
            last[1] = max(last[1], curr[1])
        else:
            merged.append(curr.copy())

    return merged
```