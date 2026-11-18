### 설명
1. **입력 검증**: 빈 입력이면 즉시 빈 리스트를 반환합니다.
2. **정렬**: 시작점을 기준으로 오름차순 정렬된 **복사본**을 생성하여 원본 리스트의 변경을 방지합니다.
3. **병합 순회**: 정렬된 구간을 앞부터 차례로 확인합니다. 현재 구간의 시작점이 결과 리스트 마지막 구간의 끝점보다 작거나 같으면(`start <= last_end`), 겹치거나 맞닿은 것이므로 끝점을 `max`로 확장하여 병합합니다. 그렇지 않으면 새로운 구간으로 추가합니다.
4. **결과의 정렬 보장**: 초기 정렬 과정에서 시작점 순서대로 처리되므로 결과 리스트는 자연스럽게 시작점 오름차순 정렬됩니다.

- 시간복잡도: `O(N log N)` (정렬 기준)
- 공간복잡도: `O(N)` (정렬 복사본 및 결과 리스트 저장)

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    # 시작점을 기준으로 정렬된 복사본 생성 (원본 불변성 보장)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0][:]]  # 첫 구간을 복사하여 결과 초기화

    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(last_end, end)
        else:                  # 중복/연속 없으면 새 구간 추가
            merged.append([start, end])

    return merged
```