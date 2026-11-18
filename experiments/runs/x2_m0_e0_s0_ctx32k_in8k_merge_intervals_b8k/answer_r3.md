입력을 시작값 기준으로 정렬한 후, 앞선 구간의 끝값과 현재 구간의 시작값을 비교하며 병합합니다. `current_start <= prev_end`이면 겹치거나 맞닿은 것이므로 최대 끝값으로 확장하고, 아니면 새 구간으로 추가합니다. 원본 데이터는 참조만 복사해 다루어 수정하지 않도록 처리했습니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작점 기준으로 정렬된 복사본 생성 (원본 불변 보장)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged = [list(sorted_intervals[0])]
    for start, end in sorted_intervals[1:]:
        prev_end = merged[-1][1]
        # 겹치거나 맞닿으면 끝값을 최대값으로 확장, 아니면 새 구간 추가
        if start <= prev_end:
            merged[-1][1] = max(prev_end, end)
        else:
            merged.append([start, end])

    return merged
```