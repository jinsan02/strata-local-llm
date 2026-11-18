### 설명
구간을 시작점 기준으로 정렬한 후 단 한 번의 순회로 병합합니다. 마지막 결과 구간과 현재 구간이 겹치거나 끝점이 맞닿으면(`start <= last_end`) 최대 끝점으로 확장하고, 그렇지 않으면 새 구간으로 추가합니다. `sorted()`와 새로운 리스트를 사용하므로 원본 입력은 안전합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 정렬된 새 리스트를 만들어 원본을 보호합니다.
    sorted_ivs = sorted(intervals, key=lambda x: x[0])
    merged = [[sorted_ivs[0][0], sorted_ivs[0][1]]]

    for start, end in sorted_ivs[1:]:
        if start <= merged[-1][1]:  # 겹치거나 끝점이 맞닿으면
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
```