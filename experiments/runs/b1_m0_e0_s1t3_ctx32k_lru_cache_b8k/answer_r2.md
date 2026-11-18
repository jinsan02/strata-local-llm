해시 맵(`dict`)과 더블 리nked list를 조합하면 키 조회와 순서 관리를 모두 O(1)에 처리할 수 있습니다.
- `dict`는 키 → 노드 매핑으로 즉시 접근을 담당합니다.
- 링크드 리스트는 사용 순서를 유지하며, 헤드 근처에 최신 사용 노드를, 테일 직전에 LRU 노드를 배치합니다.
- 가짜(head/tail) 노드로 경계 조건을 처리하면 코드 간결성을 높일 수 있습니다.
- `capacity == 0`은 초기화 시 저장 공간을 할당하지 않고 메서드 진입 시 바로 반환하도록 최적화했습니다.

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(0, capacity)
        self.cache = {}
        
        # 경계 조건 처리용 더미 노드
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        """헤드 바로 다음에 노드를 삽입합니다."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """링크드 리스트에서 특정 노드를 제거합니다."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: Node) -> None:
        """노드를 제거 후 헤드 직전에 재삽입하여 최신 사용으로 표시합니다."""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        """테일 직전(LRU) 노드를 제거하고 반환합니다."""
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if self.capacity == 0 or key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]
```