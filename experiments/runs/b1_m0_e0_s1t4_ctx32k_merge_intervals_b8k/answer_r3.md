### 설명
1. **정렬**: 시작시간을 기준으로 구간을 정렬합니다. `sorted()`는 새 리스트를 반환하므로 원본이 변경되지 않습니다.
2. **병합 순회**: 정렬된 구간을 하나씩 검사하며, 현재 구간의 시작점이 마지막 병합된 구간의 끝점보다 작거나 같으면 (`current[0] <= merged[-1][1]`) 겹치거나 맞닿은 것이므로 끝점을 큰 값으로 업데이트합니다. 그렇지 않으면 새로운 구간으로 추가합니다.
3. **불변성 보장**: `merged`에 저장할 때 슬라이스 복사(`[:]`)를 사용해 입력 리스트의 내부 배열이 변조되지 않도록 합니다.
4. **복잡도**: 시간 `O(N log N)` (정렬), 공간 `O(N)` (출력 및 정렬용 복사본).

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작점 기준 정렬 (원본 리스트는 유지)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged = [sorted_intervals[0][:]]  # 첫 구간을 복사하여 시작
    for current in sorted_intervals[1:]:
        if current[0] <= merged[-1][1]:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(merged[-1][1], current[1])
        else:                            # 새 구간 추가 (복사하여 원본 변경 방지)
            merged.append(current[:])

    return merged
```