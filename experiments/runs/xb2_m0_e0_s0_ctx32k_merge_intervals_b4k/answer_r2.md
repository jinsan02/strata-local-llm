### 설명
1. 입력이 비어있으면 즉시 빈 리스트를 반환합니다.
2. `sorted()`로 시작점 기준 정렬된 **새 리스트**를 만들어 원본 입력의 변경을 방지합니다.
3. 정렬된 구간을 순회하며 직전 병합 구간의 끝값(`last_end`)과 현재 시작값을 비교합니다. 겹치거나 맞닿은 경우(`current_start <= last_end`)에는 끝값을 두 구간 중 큰 값으로 갱신하고, 그렇지 않으면 새 구간을 결과 리스트에 추가합니다.
4. 순차적으로 처리되므로 결과 리스트는 자연스럽게 시작점 오름차순으로 정렬됩니다.

### 코드
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
        
    # 원본 입력을 변경하지 않기 위해 새 정렬 리스트 생성
    sorted_int = sorted(intervals, key=lambda x: x[0])
    
    merged = [list(sorted_int[

```