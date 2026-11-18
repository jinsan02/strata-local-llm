해시맵(dict)과 양방향 연결리스트(doubly linked list)를 조합하여 구현합니다. 해시맵은 키 탐색을 평균 O(1)로 처리하고, 연결리스트는 노드의 삽입·제거·이동을 O(1)에 수행하며 가장 최근 사용한 항목(헤드 근처)과 가장 오래 사용한 항목(테일 근처)을 상수 시간에 관리할 수 있습니다. `capacity`가 0인 경우 저장소 역할을 하지 않도록 진입 시 즉시 반환합니다. `functools.lru_cache`는 사용하지 않았습니다.

```python
class _Node:
    __slots__ = 'key', 'val', 'prev', 'next'
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(0, capacity)
        self.cache = {}  # key -> _Node
        
        # 더미 헤드/테일로 연결리스트의 양 끝 처리를 단순화합니다.
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        prev_n, next_n = node.prev, node.next
        prev_n.next = next_n
        next_n.prev = prev_n

    def _add_to_head(self, node: _Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: _Node) -> None:
        self._remove(node)
        self._add_to_head(node)

    def _pop_tail(self) -> _Node:
        res_node = self.tail.prev
        if res_node != self.head:
            self._remove(res_node)
            return res_node
        return None

    def get(self, key: int) -> int:
        if self.capacity <= 0:
            return -1
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            if len(self.cache) > self.capacity:
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
```