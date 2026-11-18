### 설명
1. 빈 입력이면 즉시 빈 리스트를 반환합니다.
2. `sorted()` 로 시작점을 기준으로 새 정렬 리스트를 생성하여 **원본 입력을 변경하지 않습니다**.
3. 정렬된 구간을 순회하며, 현재 구간의 시작점이 마지막 결과 구간의 끝점 이하(`start <= last_end`)일 경우 **겹치거나 맞닿은 상태**로 판단해 끝점을 `max` 로 확장합니다. 그렇지 않으면 새로운 구간으로 추가합니다.
4. 최종적으로 새로 생성된 리스트를 반환합니다. (시간복잡도: O(N log N), 공간복잡도: O(N))

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작점을 기준으로 정렬 (원본 리스트는 변경되지 않음)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged = []
    for start, end in sorted_intervals:
        if merged and start <= merged[-1][1]:
            # 겹치거나 맞닿으면 끝점 확장 (새로운 리스트로 덮어씌워 원본 무결성 유지)
            merged[-1] = [merged[-1][0], max(merged[-1][1], end)]
        else:
            # 새 구간 추가
            merged.append([start, end])

    return merged
```