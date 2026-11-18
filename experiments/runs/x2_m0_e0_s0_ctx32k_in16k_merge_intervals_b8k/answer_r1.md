구간 병합 문제는 **시작점을 기준으로 정렬**한 후 순회하면서 현재 구간과 직전 병합 구간의 경계를 비교하는 방식으로 해결합니다. 겹치거나 맞닿는 경우(`current_start <= last_end`)에는 끝값을 `max()`로 확장하고, 그렇지 않으면 새 구간으로 추가합니다. 원본 입력을 변경하지 않으므로 `sorted()`를 통해 정렬된 사본을 생성하고, 병합 시에도 매번 새로운 리스트 `[start, end]`를 할당하여 참조 공유 부작용을 원천 차단합니다. 시간복잡도 `O(N log N)`, 공간복잡도 `O(N)`입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작점을 기준으로 정렬 (원본 수정 방지)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    # 병합 결과를 담을 리스트 (원본 내부 리스트 참조 공유 방지)
    merged = [[sorted_intervals[0][0], sorted_intervals[0][1]]]

    for start, end in sorted_intervals[1:]:
        last_end = merged[-1][1]
        # 겹치거나 맞닿으면 끝값만 최대값으로 확장
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        # 아니면 새 구간 추가
        else:
            merged.append([start, end])

    return merged
```