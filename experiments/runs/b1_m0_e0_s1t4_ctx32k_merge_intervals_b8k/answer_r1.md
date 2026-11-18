### 동작 원리 (짧은 설명)
1. 입력이 비어있으면 즉시 빈 리스트를 반환합니다.
2. 시작점을 기준으로 구간을 정렬합니다 (`sorted` 함수는 새로운 리스트를 생성하므로 원본을 건드리지 않습니다).
3. 정렬된 구간 중 첫 번째를 새 리스트에 복사하여 추가합니다.
4. 나머지를 순회하며, 현재 구간의 시작점이 결과 리스트 마지막 구간의 끝점보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로 최대 끝점으로 확장합니다. 그렇지 않으면 새로운 구간으로 추가합니다.
5. 모든 구간 처리 후 결과를 반환합니다. (시간 복잡도: `O(N log N)`, 공간 복잡도: `O(N)`)

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작점을 기준으로 정렬 (입력 변경 방지를 위해 새 리스트 생성)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [sorted_intervals[0].copy()]

    for curr in sorted_intervals[1:]:
        if curr[0] <= merged[-1][1]:
            # 겹치거나 맞닿으면 끝점만 최대값으로 확장
            merged[-1][1] = max(merged[-1][1], curr[1])
        else:
            # 그렇지 않으면 새로운 구간 추가 (복사하여 원본 참조 방지)
            merged.append(curr.copy())

    return merged
```