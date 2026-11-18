### 설명
- **데이터 구조**: `collections.OrderedDict`를 사용합니다. Python에서 삽입/수정 시 순서를 O(1)에 유지하며, 최신 사용으로 이동(`move_to_end`)과 가장 오래된 항목 제거(`popitem(last=False)`)도 모두 평균 O(1)로 동작합니다.
- **로직**:
  - `get`: 키가 없으면 `-1`, 있으면 값을 반환하고 해당 키를 맨 뒤(최신 사용)로 이동.
  - `put`: capacity ≤ 0 이면 즉시 리턴. 기존 키면 순서만 갱신, 새 키면 저장 후 용량 초과 시 가장 앞쪽(Least Recently Used) 항목 제거.
- **시간 복잡도**: 해시 기반 접근과 OrderedDict 의 내장 연산 모두 평균 O(1) 보장.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value) -> None:
        if self.capacity <= 0:
            return
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```