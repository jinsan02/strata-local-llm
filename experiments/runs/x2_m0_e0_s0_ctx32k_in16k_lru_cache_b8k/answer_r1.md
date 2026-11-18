### 접근 방식
LRU(Least Recently Used) 캐시는 **O(1)** 시간 복잡도로 삽입/조회를 처리해야 하므로, 일반적으로 **해시 테이블 + 이중 연결리스트** 조합을 사용합니다. 파이썬에서는 `collections.OrderedDict`가 내부적으로 해시 맵과 이중 연결리스트를 함께 관리하며, `move_to_end()`로 순서 갱신과 `popitem(last=False)`로 LRU 항목 제거가 모두 O(1)이므로 표준 라이브러리만으로 요구사항을 cleanly 구현할 수 있습니다. `capacity == 0`인 경우 즉시 리턴하도록 처리하면 불필요한 저장 연산을 방지합니다.

- **시간 복잡도**: `get`, `put` 모두 평균 O(1)
- **공간 복잡도**: O(capacity)

### 최종 코드

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(0, capacity)
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key)  # 조회 시 가장 최근 사용 위치로 이동
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.cache:
            self.cache.move_to_end(key)  # 기존 키면 최근 사용으로 이동
        self.cache[key] = value          # 새 키 삽입 또는 기존 값 갱신
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # 가장 오래된 항목(LRU) 제거
```