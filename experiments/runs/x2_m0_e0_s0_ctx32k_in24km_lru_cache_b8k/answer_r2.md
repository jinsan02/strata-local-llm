Python의 `collections.OrderedDict`는 항목 삽입 순서를 보존하며, `move_to_end()`와 `popitem()` 연산이 평균 O(1)에 동작합니다. 이를 활용하여 요청사항을 충족하는 LRU Cache를 구현했습니다.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # 조회 시 해당 키를 최신 사용 순서로 이동
        return self.cache[key]

    def put(self, key, value) -> None:
        if self.capacity == 0:
            return
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # 가장 오래된(LRU) 키 제거
```