해시 맵(`dict`)과 이중 연결 리스트를 결합하여 구현합니다. 해시 맵은 키를 `O(1)`에 조회하고 노드를 참조하며, 이중 연결 리스트는 사용 순서를 `O(1)`에 유지합니다. 더미 `head`/`tail` 노드를 활용해 경계 조건을统一管理하고, `capacity`가 0인 경우 즉시 반환하도록 처리했습니다.

```python
class LRUCache:
    class Node:
        __slots__ = 'key', 'val', 'prev', 'next'
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = self.Node()  # dummy head (최근 사용)
        self.tail = self.Node()  # dummy tail (최오래 사용)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: Node) -> None:
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.val

    def put(self, key, value) -> None:
        if self.capacity <= 0:
            return
        
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            node = self.Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            
            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]
```