### 알고리즘 설명
1. 입력이 빈 리스트면 즉시 `[]`을 반환합니다.
2. 원본 데이터의 변경을 막기 위해 `sorted()`로 새 리스트를 생성한 뒤, 구간 시작점 기준 오름차순으로 정렬합니다. (시간복잡도: `O(n log n)`)
3. 정렬된 구간의 첫 번째를 결과 리스트 `merged`에 복사해 넣습니다.
4. 나머지 구간을 순회하며, 현재 구간의 시작점이 `merged`의 마지막 구간 끝점보다 작거나 같으면(겹치거나 맞닿음) 끝점을 더 큰 값으로 갱신합니다. 다르면 새로운 구간으로 추가합니다.
5. 최종적으로 정렬된 병합 결과 리스트를 반환합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 입력 원본을 변경하지 않도록 sorted()로 복사 후 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0][:]]  # 첫 구간을 새 리스트로 복사
    
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:  # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(merged[-1][1], end)
        else:                      # 별개의 구간인 경우 추가
            merged.append([start, end])
            
    return merged
```