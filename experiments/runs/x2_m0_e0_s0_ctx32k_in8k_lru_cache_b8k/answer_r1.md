해시 맵과 순서 유지 자료구조(`collections.OrderedDict`)를 조합하여 구현합니다. `OrderedDict`는 키-값 쌍의 삽입 순서를 기억하며, `move_to_end(key)`로 최신 사용 위치로의 이동과 `popitem(last=False)`로 가장 오래된(LRU) 항목 제거가 모두 평균 O(1)에 수행됩니다. capacity가 0인 경우 즉시 -1을 반환하거나 작업을 무시하여 조건을 만족합니다.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(0, capacity)
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if self.capacity == 0 or key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value
```