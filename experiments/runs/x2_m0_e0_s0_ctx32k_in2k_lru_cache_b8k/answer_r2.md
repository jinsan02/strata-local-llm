### 간략 설명
Python 표준 라이브러리인 `collections.OrderedDict`는 내부적으로 해시 테이블과 이중 연결 리스트를 조합하여 구현되어 있습니다. 키의 조회(`__getitem__`), 갱신, 이동(`move_to_end`) 및 맨 앞 항목 삭제(`popitem(last=False)`) 연산 모두 평균 **O(1)** 시간 복잡도를 보장하므로, 별도의 노드 클래스나 포인터 조작 없이도 간결하고 효율적으로 LRU 캐시를 구현할 수 있습니다. `capacity`가 0인 경우 즉시 반환하도록 조건을 분기하여 불필요한 메모리 할당과 연산을 방지했습니다.

### 최종 코드
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(capacity, 0)
        self.cache = OrderedDict() if self.capacity > 0 else {}

    def get(self, key) -> int:
        if self.capacity == 0 or key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value) -> None:
        if self.capacity == 0:
            return
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
```