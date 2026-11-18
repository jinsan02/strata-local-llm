**알고리즘 개요**
1. 원본 리스트 변경을 막기 위해 `sorted()`로 시작 시간을 기준으로 정렬한 복사본을 만듭니다.
2. 정렬된 구간들을 순회하며, 현재 구간의 시작점이 결과 리스트의 마지막 구간 끝점보다 작거나 같으면(`<=`) 겹치거나 맞닿은 것이므로 끝점을 최댓값으로 확장하여 병합합니다.
3. 그렇지 않으면 완전히 분리된 구간이므로 새 리스트로 추가합니다.
4. 정렬 및 병합 과정에서 입력 시퀀스가 순회 순서대로 처리되므로, 결과 리스트는 자연스럽게 시작점 오름차순을 유지합니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 원본 수정 방지를 위해 sorted()로 정렬된 복사본 생성
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [sorted_intervals[0].copy()]
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:          # 겹치거나 맞닿은 경우 병합
            merged[-1][1] = max(merged[-1][1], end)
        else:                               # 분리된 경우 추가
            merged.append([start, end])
            
    return merged
```