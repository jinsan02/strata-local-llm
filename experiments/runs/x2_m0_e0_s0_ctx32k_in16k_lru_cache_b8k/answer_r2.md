해시 테이블(`dict`)과 더블 리nkedList를 결합하여 구현합니다. Dictionary는 키→노드 매핑으로 `O(1)` 탐색을, Doubly Linked List는 사용 순서 관리로 선두(LRU)와 후미(MRU)에서의 `O(1)` 추가/삭제를 담당합니다. `capacity`가 0이면 즉시 종료하여 저장하지 않도록 처리하며, 노드 이동과 제거는 더미(head/tail) 노드를 활용해 경계 조건을 단순화합니다.

```python
class _Node:
    __slots__ = ('key', 'value', 'prev', 'next')
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[int | str, _Node] = {}
        
        # 더미 노드: head(LRU 끝), tail(MRU 끝)
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_tail(self, node: _Node) -> None:
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_tail(self, node: _Node) -> None:
        self._remove(node)
        self._add_to_tail(node)

    def get(self, key: int | str) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_tail(node)  # 최근 사용으로 이동
        return node.value

    def put(self, key: int | str, value: int) -> None:
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_tail(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.head.next
                self._remove(lru)
                del self.cache[lru.key]
                
            node = _Node(key, value)
            self.cache[key] = node
            self._add_to_tail(node)
```