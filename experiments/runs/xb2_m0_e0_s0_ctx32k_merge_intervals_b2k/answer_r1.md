### 설명
1. **정렬**: 입력 리스트를 시작점 기준으로 오름차순 정렬합니다. `sorted()`는 새 리스트를 반환하므로 원본을 수정하지 않습니다.
2. **병합 반복**: 정렬된 구간을 순회하며 현재 구간과 마지막 병합 구간의 끝점을 비교합니다.
   - 현재 시작점이 이전 끝점보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로, 두 구간의 끝점 중 큰 값으로 이전 구간의 끝점을 확장합니다. (병합 결과로 새 리스트를 생성해 원본 수정을 방지)
   - 아니면 완전히 새로운 구간이므로 결과 리스트에 추가합니다.
3. **시간/공간 복잡도**: 정렬 `O(n log n)`, 순회 `O(n)`. 전체 `O(n log n)` 시간, `O(n)` 공간 소요.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작점 기준으로 정렬 (원본 리스트 복사 없음, 참조만 새로 담은 리스트 생성)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    # 결과 리스트에 첫 구간을 새 리스트로 초기화 (원본 내부 리스트 수정 방지)
    result = [[sorted_intervals[0][0], sorted_intervals[0][1]]]
    
    for start, end in sorted_intervals[1:]:
        if start <= result[-1][1]:  # 겹치거나 맞닿은 경우 병합
            result[-1][1] = max(result[-1][1], end)
        else:                      # 독립적인 구간이므로 추가
            result.append([start, end])
            
    return result
```