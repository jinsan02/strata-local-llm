입력 구간을 시작점 기준으로 정렬한 후 순회하며 병합합니다. 현재 구간의 시작점이 누적된 마지막 구간의 끝점보다 작거나 같으면(중복 또는 맞닿음) 최대 끝점으로 확장하고, 그렇지 않으면 새 구간으로 추가합니다. 원본 데이터 변경을 방지하기 위해 내부를 새로운 리스트로 복사하여 처리합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 원본 수정 방지를 위해 독립적인 리스트 복사 후 시작점 기준 정렬
    work = sorted([list(interval) for interval in intervals], key=lambda x: x[0])
    merged = [work[0]]

    for start, end in work[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:  # 겹치거나 맞닿은 경우 병합
            merged[-1] = [prev_start, max(prev_end, end)]
        else:
            merged.append([start, end])

    return merged
```