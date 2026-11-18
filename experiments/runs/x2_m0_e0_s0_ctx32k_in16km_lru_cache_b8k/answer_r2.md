### 설명
Python의 표준 라이브러리인 `collections.OrderedDict`는 내부적으로 이중 연결 리스트와 해시 테이블을 함께 사용합니다. 따라서 `move_to_end()`(가장 최근 사용으로 순서 이동)와 `popitem(last=False)`(가장 오래된 항목 제거, 삽입) 연산이 모두 **평균 O(1)** 시간 복잡도를 보장합니다. 이를 활용하여 용량 제한, 접근 순서 갱신, capacity 0일 때 즉시 회피하는 조건을 처리한 LRU 캐시를 구현했습니다.

```python
from collections import OrderedDict

class LRUCache:
    """
    평균 O(1) 수행 시간을 가지는 LRU Least Recently Used Cache입니다.
    collections.OrderedDict의 삽입/접근 순서 유지 기능과 
    O(1) 이동·삭제 연산을 활용하여 구현했습니다.
    """
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity must be non-negative.")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key) -> int:
        # 용량이 0이거나 키가 없으면 즉시 -1 반환
        if self.capacity == 0 or key not in self.cache:
            return -1
        # 조회 시 해당 키를 가장 최근 사용 순서로 이동
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value) -> None:
        # 용량이 0이면 저장하지 않고 즉시 종료
        if self.capacity == 0:
            return
        
        if key in self.cache:
            self.cache.move_to_end(key)  # 기존 키 갱신 시 최신 순서로 이동
        self.cache[key] = value
        
        # 저장 후 용량을 초과하면 가장 오래 사용하지 않은 키(가장 앞쪽) 제거
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```