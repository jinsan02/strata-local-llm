해시 테이블(`dict`)과 양방향 연결리스트를 조합하여 구현합니다. 해시로 키의 존재 여부와 접근을 **O(1)**에 처리하고, 연결리스트로 사용 순서를 관리하여 선두 삽입/후미 삭제를 **O(1)**에 수행합니다. 더미(head/tail) 노드를 사용하여 경계 조건 분기를 제거하고, `capacity == 0`일 때는 저장하지 않도록 `put` 메서드에서 즉시 반환 처리합니다.

```python
class LRUCache:
    class _Node:
        def __init__(self, key: int = 0, value: int = 0):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        
        # 더미 헤드/테일 노드 (경계 조건 단순화)
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: _Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: _Node) -> None:
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _move_to_head(self, node: _Node) -> None:
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> _Node:
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = self._Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]
```