해시 맵(`dict`)과 양방향 링크 리스트를 조합하여 구현합니다. 해시 맵은 키의 `O(1)` 조회와 노드 직접 참조를 담당하고, 링크 리스트는 사용 순서(MRU ↔ LRU)를 상수 시간 내에 유지합니다. 더미 헤드/테일 노드를 적용해 경계 조건 처리를 단순화했으며, 용량 초과 시 테일 직전(LRU) 노드를 제거합니다. `capacity <= 0`인 경우 즉시 리턴하여 메모리를 할당하지 않습니다.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(0, capacity)
        self.cache = {}  # key -> Node
        
        # 더미 헤드는 가장 최근 사용(MRU), 더미 테일은 가장 오래된 사용(LRU) 위치를 가리킴
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        """더미 헤드 바로 뒤에 노드를 삽입 (MRU 위치)"""
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        node.prev = self.head

    def _remove_node(self, node: Node) -> None:
        """링크 리스트에서 특정 노드를 제거"""
        prev_n, next_n = node.prev, node.next
        prev_n.next = next_n
        next_n.prev = prev_n

    def _move_to_head(self, node: Node) -> None:
        """노드를 링크 리스트의 MRU 위치로 이동"""
        self._remove_node(node)
        self._add_to_head(node)

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.cache:
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
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            # 용량 초과 시 가장 오래 사용하지 않은 노드(LRU) 제거
            if len(self.cache) > self.capacity:
                lru = self.tail.prev
                self._remove_node(lru)
                del self.cache[lru.key]
```