### 구현 요약
- **O(1) 보장**: 해시 맵(`dict`)으로 키 조회를 O(1)에 처리하고, 더미 헤드/테일을 갖는 **이중 연결 리스트**로 사용 순서를 관리합니다.
- **순서 유지**: `get` 또는 `put` 시 해당 노드를 리스트 헤드 바로 뒤로 이동시켜 “가장 최근 사용” 상태를 반영합니다.
- **eviction**: `put` 시 용량을 초과하면 테일 바로 앞(LRU) 노드를 제거하고 맵에서 삭제합니다.
- **capacity == 0**: `put` 메서드 초기에 리턴하여 아무것도 저장하지 않도록 처리합니다.

```python
class LRUCache:
    class _Node:
        __slots__ = ('key', 'value', 'prev', 'next')
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> _Node
        
        # 더미 헤드/테일: 빈 상태·선두/말단 조작을 상수 시간에 처리
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: '_Node') -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: '_Node') -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: '_Node') -> None:
        self._remove(node)
        self._add_to_head(node)

    def _pop_tail(self) -> '_Node':
        """테일 바로 앞(LRU) 노드를 제거하고 반환"""
        node = self.tail.prev
        self._remove(node)
        return node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)  # 최근 사용으로 이동
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return  # 용량 0이면 저장 불가

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]  # 가장 오래된 항목 제거
            
            new_node = self._Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
```