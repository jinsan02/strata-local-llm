해시맵(`dict`)과 양방향 연결 리스트를 조합하여 구현합니다. 해시맵은 키로 노드를 O(1)에 접근하게 하고, 연결 리스트는 사용 순서를 유지하며 선두(MRU)와 후미(LRU)에서의 삽입/삭제를 O(1)로 처리합니다. `get` 또는 `put` 시 해당 노드를 리스트 선두로 이동시켜 최신 기록을 갱신하고, 용량 초과 시 리스트 후미의 노드(LRU)를 제거합니다. `capacity == 0`인 경우 즉시 동작을 중단합니다.

```python
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()  # 더미 헤드 (MRU 방향)
        self.tail = Node()  # 더미 테일 (LRU 방향)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
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
        if self.capacity == 0:
            return -1
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return -1

    def put(self, key, value) -> None:
        if self.capacity == 0:
            return
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]
```