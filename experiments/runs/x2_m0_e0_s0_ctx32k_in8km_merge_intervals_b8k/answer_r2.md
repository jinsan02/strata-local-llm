입력을 시작점 기준으로 정렬한 후, 앞선 누적 구간과 현재 구간이 겹치거나 맞닿으면 끝값을 확장하고, 그렇지 않으면 새로운 구간으로 추가합니다. 입력 객체를 보호하기 위해 정렬된 시퀀스와 결과 리스트의 요소를 별도로 복사하여 구성하며, 시간 복잡도는 `O(N log N)`입니다.

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # 시작점을 기준으로 정렬된 새로운 리스트 생성 (원본 입력 보호)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    result = [list(sorted_intervals[0])]
    
    for curr in sorted_intervals[1:]:
        if curr[0] <= result[-1][1]:
            # 겹치거나 맞닿은 경우: 결과의 마지막 구간에 끝값을 더 큰 쪽으로 확장
            result[-1][1] = max(result[-1][1], curr[1])
        else:
            # 새로운 구간이므로 복사하여 추가
            result.append(list(curr))
            
    return result
```