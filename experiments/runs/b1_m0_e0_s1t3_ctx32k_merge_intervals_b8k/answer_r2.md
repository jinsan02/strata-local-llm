입력을 시작점 기준으로 정렬한 후 순회하며 겹치거나 맞닿은 구간은 최대 종료점까지 확장하고, 그렇지 않으면 새로운 구간으로 추가합니다. 원본 리스트 변경을 방지하기 위해 정렬 시 `sorted()`를 사용하고 병합 결과에는 새 리스트를 생성합니다. 시간 복잡도는 `O(n log n)`입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(merged[-1][1], end)
        else:                       # 별개 구간인 경우 추가
            merged.append([start, end])

    return merged
```