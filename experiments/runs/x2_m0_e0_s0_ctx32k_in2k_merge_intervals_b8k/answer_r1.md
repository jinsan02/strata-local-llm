### 설명
1. 빈 입력이면 즉시 빈 리스트를 반환합니다.
2. 원본 데이터를 변경하지 않기 위해 시작 시간(`start`) 기준으로 정렬한 새 리스트를 생성합니다.
3. 정렬된 구간을 순회하며 마지막 병합 결과와 비교합니다. 현재 구간의 시작점이 마지막 끝점보다 작거나 같으면(겹치거나 맞닿음) `max()`로 끝점을 갱신하여 병합하고, 그렇지 않으면 새로운 구간으로 복사해 추가합니다.
4. 전체 시간 복잡도는 정렬 기준 `O(N log N)`, 보조 공간은 `O(N)` 입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 원본 변경 방지 + 시작점 기준 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]  # 첫 구간 복사본으로 초기화

    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:          # 겹치거나 맞닿은 경우 병합
            last[1] = max(last[1], current[1])
        else:                              # 분리된 경우 새로운 구간 추가
            merged.append(list(current))

    return merged
```